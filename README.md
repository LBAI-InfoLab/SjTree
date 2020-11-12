# **SjTree**
SjTree is a tool to analyze the normalized expression value of the variance stabilization transformation (VST) of RNAseq data. It is built around a composite model based on decision trees. The composition of this model may change based on future work, but the current implementation will still be available, along with all of these possible iterations. Data interpolation work is still ongoing and we are currently evaluating different strategies to enable deployment of this tool on different datasets.

## **Script usage**

### System requirements
SjTree runs on the Linux distribution (tested on Ubuntu 20.04 LTS) and requires python 3.7. + With the packages listed in the requirements.txt file. We recommend hardware with at least 2+ GB of RAM for this program for minimum performance and 12+ GB for optimum performance.

### Installation guide
The installation procedure (including installing the required dependencies) should take less than 5 minutes with an internet speed of 5 Mbps or more.

Clone the current directory on your computer
> git clone https://github.com/LBAI-InfoLab/SjTree.git

Go the downloaded directory
> cd SjTree/

(optional) install SjTree as a python module
> python setup.py install

Install the required dependencies
> pip install -r requirements.txt

### Usage
Navigate to the program directory, you should see a SjTree.py file that you can use as a python script.
> python SjTree.py -h

### Arguments
* --ifile / -i : the input file, dataset to process
* --ofile / -o : name of the output file to generate
* --interp / -p : set to False to skip interpolation (optionnal)
* --help / -h : display help

### Ouput
In addition to the predictions (stored in the user-defined output file), SjTree create a cluster distribution figure (.png file) and an AFD representation of clusters (.gif) in the images subfolder.

### Example
To run SjTree on your own data, use the following line:
> python SjTree.py --ifile my_data_file.csv --ofile my_result_file.csv

## Demo
The "example" folder contains a file with anonymized data from the original study and the associated expected results. You can test the software using the following command line:

> python SjTree.py --ifile example/example_dataset.csv --ofile predictions.csv --interp False

You can then check that the predictions correspond to the expected results (available in the example folder). The script should take approximately 40 seconds to run on a computer with the recommended configuration.


## **Data structure**
### Mandatory columns
The input file must be a csv file containing at least the following columns:
* ID
* NAPA
* RSPH9
* TMEM92
* OAS1
* MXD3
* USP18
* ILK
* GTPBP2
* PI4K2B
* RP11.295G20.2
* ZNF318
* IFI27
* MMP25
* STIL
* MX1
* LINC01001
* NCF4
* WDR89
* LIMK2
* CCT2
* ZCCHC2
* HERC5
* DHX58
* USP32
* PGS1
* ANXA3
* OASL
* BCORL1
* IFI44L
* TLR1
* KCNJ2
* CHST15
* HAL
* YKT6
* CLUAP1
* TBL1X
* CACUL1
* KIAA1045
* THADA
* ETS2

## Model composition

### C4 Detector

![Alt text](images/C4_detector_tree_1.jpeg?raw=true "Predictor 1")
![Alt text](images/C4_detector_tree_2.jpeg?raw=true "Predictor 2")
![Alt text](images/C4_detector_tree_3.jpeg?raw=true "Predictor 2")

### C1C2C3 Classifier

#### C1
![Alt text](images/C1C2C3_C1_classifier_tree_1.jpeg?raw=true "Predictor 1")
![Alt text](images/C1C2C3_C1_classifier_tree_2.jpeg?raw=true "Predictor 2")
![Alt text](images/C1C2C3_C1_classifier_tree_3.jpeg?raw=true "Predictor 3")
![Alt text](images/C1C2C3_C1_classifier_tree_4.jpeg?raw=true "Predictor 4")

#### C2
![Alt text](images/C1C2C3_C2_classifier_tree_1.jpeg?raw=true "Predictor 1")
![Alt text](images/C1C2C3_C2_classifier_tree_2.jpeg?raw=true "Predictor 2")
![Alt text](images/C1C2C3_C2_classifier_tree_3.jpeg?raw=true "Predictor 3")
![Alt text](images/C1C2C3_C2_classifier_tree_4.jpeg?raw=true "Predictor 4")

#### C3
![Alt text](images/C1C2C3_C3_classifier_tree_1.jpeg?raw=true "Predictor 1")
![Alt text](images/C1C2C3_C3_classifier_tree_2.jpeg?raw=true "Predictor 2")
![Alt text](images/C1C2C3_C3_classifier_tree_3.jpeg?raw=true "Predictor 3")
![Alt text](images/C1C2C3_C3_classifier_tree_4.jpeg?raw=true "Predictor 4")

