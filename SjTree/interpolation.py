


def extract_balise(dataset):
    """
    Extract balise gene and their associated value,
    take the mean of the column
    """

    ## importation
    import pandas as pd

    ## parameters
    target_genes = [
        "NUP210L",
        "SPIRE1",
        "GATAD1",
        "HVCN1",
        "ENO1",
        "FLNA"
    ]

    ## load dataset
    df = pd.read_csv(dataset)

    ## try to extract target genes
    try:
        df = df[target_genes]
    except:
        print("[!] ERROR, missing genes in "+str(dataset))
        return 0

    ## compute mean of target genes
    gene_to_mean = {}
    for gene in target_genes:
        gene_to_mean[gene] = df[gene].mean()

    ## return
    return gene_to_mean



def save_balise(ref_dataset, target_dataset):
    """
    Extract gene balise for ref_dataset and target_dataset,
    save results in pickle stuff
    """

    ## importation
    import pickle

    ## extract gene to mean to ref
    gene_to_mean_ref = extract_balise(ref_dataset)

    ## extract gene to mean to target
    gene_to_mean_target = extract_balise(target_dataset)

    ## save dict in picle format
    with open('ressources/gene_to_mean_ref.pickle', 'wb') as handle:
        pickle.dump(gene_to_mean_ref, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('ressources/gene_to_mean_target.pickle', 'wb') as handle:
        pickle.dump(gene_to_mean_target, handle, protocol=pickle.HIGHEST_PROTOCOL)



def interpolate(x):
    """
    inertpolate value x from target_dataset to ref_dataset
    """

    ## importation
    import pickle
    import numpy as np

    ## load dictionnary
    with open('ressources/gene_to_mean_ref.pickle', 'rb') as handle:
        gene_to_mean_ref = pickle.load(handle)
    with open('ressources/gene_to_mean_target.pickle', 'rb') as handle:
        gene_to_mean_target = pickle.load(handle)

    ## locate x interval
    a_gene = "NA"
    b_gene = "NA"
    cmpt = 0
    gene_list = list(gene_to_mean_target.keys())
    for gene in gene_list:
        if(cmpt+1 < len(gene_list)):
            a_value = gene_to_mean_target[gene]
            b_value = gene_to_mean_target[gene_list[cmpt+1]]
            if(x >= a_value and x <= b_value):
                a_gene = gene
                b_gene = gene_list[cmpt+1]
        cmpt +=1

    ## compute interpolation
    if(a_gene != "NA" and b_gene != "NA"):
        y = gene_to_mean_ref[a_gene] + (gene_to_mean_ref[b_gene] - gene_to_mean_ref[a_gene])*((x - gene_to_mean_target[a_gene])/(gene_to_mean_target[b_gene]-gene_to_mean_target[a_gene]))

    elif(x <= gene_to_mean_target[gene_list[0]]):
        y = gene_to_mean_ref[gene_list[0]]
    elif(x >= gene_to_mean_target[gene_list[-1]]):
        y =  gene_to_mean_ref[gene_list[-1]]
    elif(np.isnan(x)):
        y = np.nan

    ## return interpolated value
    return y




def run_interpolation(ref_dataset, target_dataset, output_filename, shutup_mode):
    """
    main run
    extract and save gene balise
    extract selected genes
    load target dataset
    apply interpolate function on each entry of the target dataset
    save dataset
    """

    ## importation
    import pandas as pd
    import numpy as np

    ## parameters
    feature_file = "ressources/features.csv"

    ## display information if needed
    if(not shutup_mode):
        print("[+] Run interpolation")

    ## save gene balise
    save_balise(ref_dataset, target_dataset)

    ## extract selected genes
    selected_genes = pd.read_csv(feature_file)
    selected_genes_list = list(selected_genes['FEATURES'])

    ## load dataset
    df = pd.read_csv(target_dataset)

    ## select variables
    df_selected = pd.DataFrame()
    for var in selected_genes_list:
        try:
            df_selected[var] = df[var]
        except:
            df_selected[var] = np.nan
    df_selected['ID'] = df['ID']
    df_selected = df_selected.set_index('ID')

    ## apply interpolate function on each entry of the dataset
    df_selected = df_selected.applymap(interpolate)

    ## save dataset
    df_selected.to_csv(output_filename)

    ## display information if needed
    if(not shutup_mode):
        print("[+] Interpolation done")
