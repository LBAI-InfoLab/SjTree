

def filter_spotted_C4(X_data, y_data, preds):
    """
    Get rids of predicted C4 patients
    """

    ## add Spot C4 column
    X_data['Spot_C4'] = preds

    ## drop spoted C4
    X_data = X_data[X_data['Spot_C4'].isin([0])]

    ## drop spoted C4 column
    X_data = X_data.drop(columns=['Spot_C4'])

    ## deal with y
    updated_label = []
    cmpt = 0
    for y in y_data:
        if(preds[cmpt] == 0):
            updated_label.append(y)
        cmpt +=1

    ## return dataframe
    return X_data, updated_label


def preprocess_data(dataframe, feature_file):
    """
    use only features present in feature_file
    """

    ## importation
    import pandas as pd

    ## load features
    df_features = pd.read_csv(feature_file)
    feature_list = list(df_features['FEATURE'])

    ## check that features are present in dataset
    for f in feature_list:
        if(f not in list(dataframe.keys())):
            print("[!] ERROR => feature "+str(f)+" not found in dataset")
            return None

    ## select features in dataset
    dataframe = dataframe[feature_list]

    ## return preprocess data
    return dataframe


def assemble_prediction(C4_prediction, mult_prediction):
    """
    assemble prediction of C4 and multi models
    """

    ## parameters
    global_prediction = []
    cmpt = 0

    ## fusion list
    for pred in C4_prediction:
        if(pred == 1):
            global_prediction.append(4)
        else:
            cluster = mult_prediction[cmpt]+1
            global_prediction.append(cluster)
            cmpt +=1

    ## return global_prediction
    return global_prediction



def plot_model_tree():
    """
    """

    ## importation
    import joblib
    import matplotlib.pyplot as plt
    import xgboost as xgb

    ## parameters
    C4_model_file = "models/C4_model.model"
    multiclass_model_file = "models/C1C2C3.model"

    ## load models
    C4_detector = joblib.load(C4_model_file)
    multi_classifier = joblib.load(multiclass_model_file)

    ## generate figure for C4
    dump_list = C4_detector.get_booster().get_dump()
    num_trees = len(dump_list)
    for x in range(0,num_trees):
        xgb.plot_tree(C4_detector,num_trees=x)
        plt.tight_layout()
        plt.savefig("images/C4_detector_tree_"+str(x)+".png", dpi=600)
        plt.close()

    ## generate figure for multi
    dump_list = multi_classifier.get_booster().get_dump()
    num_trees = len(dump_list)
    for x in range(0,num_trees):
        xgb.plot_tree(multi_classifier,num_trees=x)
        plt.tight_layout()
        plt.savefig("images/C1C2C3_classifier_tree_"+str(x)+".png", dpi=600)
        plt.close()




def plot_cluster_distribution(prediction):
    """
    plot prediction
    """

    ## importation
    import matplotlib.pyplot as plt
    import numpy as np

    ## parameters
    ref_to_count_disc = {"C1":79, "C2":60, "C3":66, "C4":22}
    ref_to_count_all = {"C1":101, "C2":77, "C3":88, "C4":38}

    ## craft figure
    cluster_to_count = {"C1":0, "C2":0, "C3":0, "C4":0}
    for p in prediction:
        if(p == 1):
            cluster_to_count["C1"] += 1
        elif(p==2):
            cluster_to_count["C2"] += 1
        elif(p==3):
            cluster_to_count["C3"] += 1
        elif(p==4):
            cluster_to_count["C4"] += 1

    ## craft simple distribution
    plt.bar(cluster_to_count.keys(), cluster_to_count.values())
    plt.savefig("images/cluster_proportion.png")
    plt.close()

    ## craft compared distribution
    # set width of bar
    barWidth = 0.25

    # set height of bar
    bars1 = cluster_to_count.values()
    bars2 = ref_to_count_disc.values()

    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]

    # Make the plot
    plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='Array')
    plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='Discovery')

    # Add xticks on the middle of the group bars
    plt.xlabel('Cluster', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars1))], ['C1', 'C2', 'C3', 'C4'])

    # Create legend & Show graphic
    plt.legend()
    plt.savefig("images/cluster_proportion_compared.png")
    plt.close()









def run(data_file, shutup_mode):
    """
    """

    ## importation
    import pandas as pd
    import joblib
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import confusion_matrix
    import matplotlib.pyplot as plt

    ## silence pandas warning
    pd.options.mode.chained_assignment = None

    ## parameters
    C4_model_file = "models/C4_model.model"
    multiclass_model_file = "models/C1C2C3.model"

    ## Load dataset
    df_data = pd.read_csv(data_file)
    patient_id = df_data['ID']
    X = df_data.drop(columns=['ID'])
    y = df_data['ID']
    y['preds'] = "NA"
    y = list(y['preds'])
    patient_id = list(df_data['ID'])

    ## display information if needed
    if(not shutup_mode):
        print("[+] Run prediction")


    ##------------##
    ## PREDICTION ##############################################################
    ##------------##

    ## 1. Call First Model
    # -> prepocess data for model
    C4_X = preprocess_data(X, "ressources/C4_features.csv")

    # -> Load model
    C4_detector = joblib.load(C4_model_file)

    # -> Guess if observation is C4 or not
    C4_preds = C4_detector.predict(C4_X)

    ## save prediction results

    ## update dataset
    # -> drop patient predicted as C4
    X, y = filter_spotted_C4(X, y, C4_preds)

    ## 2. Call Main Model
    #-> preprocess data for model
    X = preprocess_data(X, "ressources/multi_features.csv")

    #-> load model
    multi_classifier = joblib.load(multiclass_model_file)

    # -> Multiclassification between C1,C2,C3
    multi_preds = multi_classifier.predict(X)

    ## assemble predictions of the model
    global_prediction = assemble_prediction(C4_preds, multi_preds)

    ## check distribution
    plot_cluster_distribution(global_prediction)

    ## create manifest file
    manifest_file = open('dataset/prediction.csv', 'w')
    manifest_file.write("ID,PREDICTION\n")
    cmpt = 0
    for pred in global_prediction:
        line_to_write = str(patient_id[cmpt])+","+str(pred)
        manifest_file.write(line_to_write+"\n")
        cmpt +=1
    manifest_file.close()

    ## display information if needed
    if(not shutup_mode):
        print("[+] Prediction done")



## TEST
#run("ressources/test_dataset_selected_features.csv")
#plot_model_tree()
