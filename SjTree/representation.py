


def prepare_dataset(dataset, manifest):
    """
    assemble datasat and its label obtained from
    model prediction, drop columns that contain NaN
    """

    ## importation
    import pandas as pd

    ## craft output_filename
    output_filename = dataset.replace(".csv", "_labeled.csv")

    ## load dataset
    df_data = pd.read_csv(dataset)
    df_data = df_data.set_index('ID')

    ## load manifest
    df_cluster = pd.read_csv(manifest)

    ## merge
    result = df_data.join(df_cluster.set_index('ID'))

    ## drop columns conatining NA
    result = result.dropna(axis='columns')

    ## save dataset
    result.to_csv(output_filename)






def craft_afd_plot(dataset):
    """
    Create AFD and save a gif representation
    """

    ## importation
    import pandas as pd
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation
    from joblib import dump

    ## parameters
    cluster_name = ["C1", "C2", "C3", "C4"]
    plt.style.use('dark_background')

    ## load dataset
    X_data = pd.read_csv(dataset)
    y = np.array(X_data['PREDICTION'])
    X = X_data.drop(columns=['ID', 'PREDICTION'])

    ## check that we have the four clusters before craft a LDA
    all_clusters_are_present = True
    for c in cluster_name:
        if(c not in list(y)):
            all_clusters_are_present = False

    ## craft representation
    if(all_clusters_are_present):

        ## init LDA
        lda = LinearDiscriminantAnalysis(n_components=3)
        X_r2 = lda.fit(X, y).transform(X)

        ## Display results
        colors = ['firebrick', 'mediumseagreen', 'dodgerblue', 'darkorange']
        fig = plt.figure()
        ax = Axes3D(fig)
        for color, i, cluster_name in zip(colors, [1, 2, 3, 4], cluster_name):
            ax.scatter(X_r2[y == i, 0], X_r2[y == i, 1], X_r2[y == i, 2], alpha=.8, color=color,
                        label=cluster_name)
        plt.legend(loc='best', shadow=False, scatterpoints=1)
        plt.title("Cluster Dispersion")

        ## save animation
        def rotate(angle):
            ax.view_init(azim=angle)
        rot_animation = animation.FuncAnimation(fig, rotate, frames=np.arange(0, 662, 1), interval=90)
        rot_animation.save('images/AFD_representation.gif', dpi=100, writer='Pillow')



## TESTS
"""
dataset = "/home/bran/Workspace/SERVIER/article_dataset/RNAseq/rnaseq_inception_prediction_dataset.csv"
manifest = "/home/bran/Workspace/SERVIER/article_analysis/xgboost/multimodel/C4_outer/prediction.csv"
prepare_dataset(dataset, manifest)
craft_afd_plot("/home/bran/Workspace/SERVIER/article_dataset/RNAseq/rnaseq_inception_prediction_dataset_labeled.csv")
"""
#craft_afd_plot("/home/bran/Workspace/SERVIER/article_dataset/inception_255genes_labeled.csv")
#craft_afd_plot("/home/bran/Workspace/SERVIER/article_dataset/inception_model_labeled.csv")
#craft_afd_plot("/home/bran/Workspace/SERVIER/article_dataset/RNAseq/rnaseq_inception_prediction_dataset_labeled.csv")
#craft_afd_plot("/home/bran/Workspace/SERVIER/article_dataset/RNAseq/PreciseSADS_RNASeq_SJS_Inception_72genes_labeled.csv")
