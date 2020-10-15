"""
DOC
"""


##-----------##
## FUNCTIONS ##
##-----------##

def check_input_format(input_file):
    """
    - check if input file exist
    - try to load input data file if it exists
    - look for expected columns if load succeed
    - return check status and log message

    TODO : actually put something as expected colmuns !
    """

    ## importation
    import pandas as pd
    import os

    ## parameters
    good_format = True
    log_message = "Everything is Ok"
    expected_columns = []

    ## check if input file exist
    if(not os.path.isfile(input_file)):
        good_format = False
        log_message = "File "+str(input_file)+" does not exist."

    ## try to load input data file if it exists
    else:
        try:
            df = pd.read_csv(input_file)
        except:
            good_format = False
            log_message = "Failed to load "+str(input_file)+"."

        ## look for expected columns if load succeed
        if(good_format):
            missing_cols = []
            cols = list(df.columns)
            for ec in expected_columns:
                if(ec not in cols):
                    missing_cols.append(ec)

            if(len(missing_cols) > 0):
                good_format = False
                log_message = "The following variables are missing: "
                for v in missing_cols:
                    log_message += str(v)+", "
                log_message = log_message[:-2]

    ## return check status and log message
    return (good_format, log_message)




def display_help():
    """
    Display doc for the programm
    """

    print("""
    SJtree take 3 arguments:
        -ifile : the name of the input data file
        -ofile : the name of the output file

        exemple of use : [FIX EXEMPLE]

        => the input file must follow a specific format to be interpreted,
           the following columns must be present:
           -> [FIX COL NAMES]
        => the generated output file is a csv file

    Require the folling packages:
        - xgboost
        - pandas
        - joblib
    """)



def run(input_data_file, output_filename):
    """
    """

    ## importation
    import preprocessing
    import interpolation
    import predictor
    import representation
    import shutil

    ## parameters
    shutup_mode = False
    interpolation_ref_dataset = "ressources/test_dataset.csv"
    interpolated_filename = "dataset/interpolated_dataset.csv"
    prediction_filename = "dataset/prediction.csv"
    representation_dataset = "dataset/interpolated_dataset_labeled.csv"

    ## preprocess data
    if(preprocessing.check_essential_variables(input_data_file, shutup_mode)):

        ## select variables
        preprocessing.select_variable(input_data_file, shutup_mode)
        preprocess_file = input_data_file.replace(".csv", "_selected_features.csv")

        ## perform interpolation
        interpolation.run_interpolation(
            interpolation_ref_dataset,
            preprocess_file,
            interpolated_filename,
            shutup_mode
        )

        ## make prediction
        predictor.run(interpolated_filename, shutup_mode)

        ## generate figures
        representation.prepare_dataset(interpolated_filename, prediction_filename)
        representation.craft_afd_plot(representation_dataset)

        ## save preds file to output_filename
        shutil.copy(prediction_filename, output_filename)

        ## display information if needed
        if(not shutup_mode):
            print("[*] Result file available : "+str(output_filename))

    else:
        ## display something for the error
        print("[ERROR] => can't process file "+str(input_data_file))



















##------##
## MAIN ##
##------##
if __name__=='__main__':

    ## importation
    import sys
    import getopt
    from colorama import init
    init(strip=not sys.stdout.isatty())
    from termcolor import cprint
    from pyfiglet import figlet_format

    ## catch arguments
    argv = sys.argv[1:]

    ## parse arguments
    input_data_file = ''
    output_filename = ''
    model_filename = ''
    try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
       display_help()
       sys.exit(2)
    for opt, arg in opts:
       if opt in ('-h', '--help'):
           display_help()
           sys.exit()
       elif opt in ("-i", "--ifile"):
          input_data_file = arg
       elif opt in ("-o", "--ofile"):
          output_filename = arg

    ## display cool banner
    text="SJtree - Cluster Prediction"
    cprint(figlet_format(text, font="standard"), "blue")

    ## check that all arguments are present
    if(input_data_file == ''):
        print("[!] No input file detected")
        print("[!] Use -h or --help options to get more informations")
        sys.exit()
    if(output_filename == ''):
        print("[!] No output file detected")
        print("[!] Use -h or --help options to get more informations")
        sys.exit()


    ## perform run
    run(input_data_file, output_filename)
