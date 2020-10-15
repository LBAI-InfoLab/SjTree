# **SjTree**
SjTree is a tool to analyse variance stabilizing transformation (VST) normalized expression value of RNAseq data. Its build around a  meta model based on xgboosted trees.

## **Script usage**

### Installation
Clone the current directory on your computer
> git clone https://github.com/LBAI-InfoLab/SjTree.git

Install the required dependencies
> pip install -r requirements.txt

### Utilisation
Go to the programm directory, you should see a SjTree.py file that you can use
as a python script.

> python3 SjTree.py -h

### Arguments
* --ifile / -i : the input file, dataset to process
* --ofile / -o : name of the output file to generate
* --help / -h : display help

### Example

> python3 SjTree.py --ifile my_data_file.csv --ofile my_result_file.csv


## **Package usage**
Work In Progress


## **Data structure**
### Mandatory columns
The input file have to be a csv file containing at least the following columns:
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
