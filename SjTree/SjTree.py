"""
SjTree
"""

##-----------##
## FUNCTIONS ###################################################################
##-----------##



def display_help():
    """
    Display help for the programm
    """

    print("""
    SjTree take 2 arguments:
        --ifile : the name of the input data file
        --ofile : the name of the output file

        exemple of use : python -i /my/input/file -o output.csv

        => the input file must follow a specific format to be interpreted,
           check README.md to have the list of mandatory variables.
        => the generated output file is a csv file

    Require the folling packages:
        - xgboost
        - pandas
        - joblib
    """)



def run(input_data_file, output_filename):
    """
    Main function, run the prediction process
        - input_data_file is a string, the name of the input file
        - output_filename is a stringn the name of the output file
    """

    ## importation
    import preprocessing
    import interpolation
    import predictor
    import representation
    import shutil

    ## parameters
    verbose_mode = True
    interpolated_filename = "dataset/interpolated_dataset.csv"
    prediction_filename = "dataset/prediction.csv"
    representation_dataset = "dataset/interpolated_dataset_labeled.csv"

    ## preprocess data
    if(preprocessing.check_essential_variables(input_data_file, verbose_mode)):

        ## select variables
        preprocessing.select_variable(input_data_file, verbose_mode)
        preprocess_file = input_data_file.replace(".csv", "_selected_features.csv")

        ## perform interpolation
        interpolation.run_interpolation(
            preprocess_file,
            interpolated_filename,
            verbose_mode
        )

        ## make prediction
        predictor.run(interpolated_filename, verbose_mode)

        ## generate figures
        representation.prepare_dataset(interpolated_filename, prediction_filename)
        representation.craft_afd_plot(representation_dataset)

        ## save preds file to output_filename
        shutil.copy(prediction_filename, output_filename)

        ## display information if needed
        if(verbose_mode):
            print("[*] Result file available : "+str(output_filename))

    else:
        ## display something for the error
        print("[ERROR] => can't process file "+str(input_data_file))




##------##
## MAIN ########################################################################
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
