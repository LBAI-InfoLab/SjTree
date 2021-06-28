

def check_essential_variables(data_file, verbose_mode):
    """
    Check if essential variables for the models are present in
    the data_file.
        - data_file is a string, the name of the file to check
        - verbose_mode is a boolean, usually set to True

    => return a boolean (False if failed, True if succeed)
    """

    ## importation
    import pandas as pd

    ## parameters
    pass_check = True
    feature_file = "ressources/essential_features.csv"

    ## display information if needed
    if(verbose_mode):
        print("[+] Look for essential variables ...")

    ## perform check
    try:
        ## load dataset
        df = pd.read_csv(data_file)

        ## extract variables to search
        df_var = pd.read_csv(feature_file)
        var_list = list(df_var['FEATURE'])
        var_list.append('ID')

        ## loop over var in dataset
        for var in var_list:
            if(var not in list(df.keys())):
                pass_check = False
                if(not verbose_mode):
                    print("[WARNING] => "+str(var)+" not found in dataset")

    except:
        print("[ERROR] => can't load "+str(data_file))
        pass_check = False

    ## return a boolean
    return pass_check



def select_variable(data_file, verbose_mode):
    """
    Craft a subset of data_file using features mandatory for the models, save
    this subset in a new csv file.
        - data_file is a string, name of the input file
        - verbose_mode is a boolean, usually set to True
    """

    ## importation
    import pandas as pd
    import numpy as np

    ## parameters
    feature_file = "ressources/features.csv"

    ## display information if needed
    if(verbose_mode):
        print("[+] Reformat "+str(data_file))

    ## craft output filename
    output_filename = data_file.replace(".csv", "_selected_features.csv")

    ## load dataset
    df = pd.read_csv(data_file)

    ## extract variables
    df_var = pd.read_csv(feature_file)
    var_list = list(df_var['FEATURES'])

    ## fill missing var with nan
    for var in var_list:
        if(var not in list(df.keys())):
            df[var] = np.nan

    ## select variables
    df = df[var_list]

    ## write resuls
    df.to_csv(output_filename, index=False)

    ## display information if needed
    if(verbose_mode):
        print("[+] File reformated")
