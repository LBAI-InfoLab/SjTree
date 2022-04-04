


def hunt_balise(data_file_name):
    """
    """

    ## importation
    import pandas as pd
    import numpy as np
    import pickle

    ## parameters
    var_to_mean1 = {}
    var_to_std1 = {}
    var_to_mean2 = {}
    var_to_std2 = {}
    std_treshold = 0.5
    max_std_treshold = 3
    std_step = 0.5
    std_selection_1 = []
    std_selection_2 = []
    final_selection = []
    mandatory_gene_file_name = "ressources/essential_features.csv"


    ## load data_file_2
    df2 = pd.read_csv(data_file_name)

    ## get mean for each var in ref
    ## get variance for each var ref
    ## load dictionnary
    with open('ressources/all_gene_to_mean_ref.pickle', 'rb') as handle:
        var_to_mean1 = pickle.load(handle)
    with open('ressources/all_gene_to_std_ref.pickle', 'rb') as handle:
        var_to_std1 = pickle.load(handle)

    ## compute mean for each var in data 2
    ## compute variance for each var in data 2
    for k in df2.keys():
        var_to_mean2[k] = np.mean(df2[k])
        var_to_std2[k] = np.std(df2[k])

    ## order data to mean 1
    var_to_mean1 = {k: v for k, v in sorted(var_to_mean1.items(), key=lambda item: item[1])}

    ## order data to mean 2
    var_to_mean2 = {k: v for k, v in sorted(var_to_mean2.items(), key=lambda item: item[1])}


    ## INIT EXPLORATION
    valid_interpolation = False
    while(not valid_interpolation and std_treshold < max_std_treshold):

        ## select var with variance below trehsold in 1
        for var in var_to_std1.keys():
            std = var_to_std1[var]
            if(std <= std_treshold):
                std_selection_1.append(var)

        ## select var with variance below treshold in 2
        for var in var_to_std2.keys():
            std = var_to_std2[var]
            if(std <= std_treshold):
                std_selection_2.append(var)

        ## compute intersection selection
        intersection = []
        for var in std_selection_1:
            if(var in std_selection_2):
                intersection.append(var)

        ## keep only selected var in var to mean 1
        mean_values_1 = []
        for var in var_to_mean1.keys():
            if(var in intersection):
                mean_values_1.append(var)

        ## keep only selected var in var to mean 2
        mean_values_2 = []
        for var in var_to_mean2.keys():
            if(var in intersection):
                mean_values_2.append(var)

        ## check that keys 1 is equal to keys 2
        ## if this is not the case loop over keys 1 and keys 2 to spot the differences
        #-> create list of differences
        diff_list = []
        if(mean_values_1 == mean_values_2):
            final_selection = mean_values_1

        else:
            cmpt = 0
            for v1 in mean_values_1:
                if(v1 != mean_values_2[cmpt] and v1 not in diff_list):
                    diff_list.append(v1)
                cmpt+=1

        ## drop differences
        final_selection = []
        for var in mean_values_1:
            if(var not in diff_list):
                final_selection.append(var)


        ## check coverage - concerned target dataset (dataset 2)
        low_list = []
        high_list = []
        range_list = []

        #-> get lowest and highest balise mean
        min_mean = var_to_mean2[final_selection[0]]
        max_mean = var_to_mean2[final_selection[-1]]

        #-> loop over var to mean in dataset2
        for var in var_to_mean2.keys():

            #-> evaluate mean & update low and high list
            mean = var_to_mean2[var]
            if(mean < min_mean):
                low_list.append(var)
            elif(mean > max_mean):
                high_list.append(var)
            else:
                range_list.append(var)

        ## check that mandatory var are not in low or high list
        missed_genes = []
        df_mandatory = pd.read_csv(mandatory_gene_file_name)
        for gene in list(df_mandatory['FEATURE']):
            if(gene not in range_list):
                missed_genes.append(gene)

        ## check that all is ok
        if(len(missed_genes) == 0):
            valid_interpolation = True
        else:
            std_treshold += std_step

    ## final check
    if(not valid_interpolation):
        print("[!][INTERPOLATION] => Failed to find suitable genes with maximum std set at 5")
        print("[!][INTERPOLATION] => Genes below covered range : ")
        for gene in low_list:
            print("[-]\t- "+str(gene))
        print("[!][INTERPOLATION] => Genes above covered range : ")
        for gene in high_list:
            print("[-]\t- "+str(gene))
    else:
        print("[*][INTERPOLATION] => Done with std of "+str(std_treshold))


    ## craft output sructure
    gene_to_mean_ref = {}
    gene_to_mean_target = {}
    for var in final_selection:
        gene_to_mean_ref[var] = var_to_mean1[var]
        gene_to_mean_target[var] = var_to_mean2[var]
    with open('ressources/gene_to_mean_ref.pickle', 'wb') as handle:
        pickle.dump(gene_to_mean_ref, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('ressources/gene_to_mean_target.pickle', 'wb') as handle:
        pickle.dump(gene_to_mean_target, handle, protocol=pickle.HIGHEST_PROTOCOL)

    ## return interpolation success state
    return valid_interpolation


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
    Intertpolate value x from target to projection domain
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




def run_interpolation(target_dataset, output_filename, verbose_mode):
    """
    Run interpolation on target dataset

        - target_dataset is a string, the name of the dataset to interpolate
        - output_filename is a string, the name of the interpolated dataset
        - verbose_mode is a boolean, usually set to True

    -> extract selected genes
    -> load target dataset
    -> apply interpolate function on each entry of the target dataset
    -> save interpolated dataset
    """

    ## importation
    import pandas as pd
    import numpy as np

    ## parameters
    feature_file = "ressources/features.csv"

    ## display information if needed
    if(verbose_mode):
        print("[+] Run interpolation")

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
    if(verbose_mode):
        print("[+] Interpolation done")
