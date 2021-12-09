# import openbabel
from openbabel import openbabel
import pandas as pd
from extract import removeAllInFolder


def getColumnData(file_name, column_name):
    fields = [column_name]
    df = pd.read_csv(file_name, skipinitialspace=True, usecols=fields)
    data = (list(df[column_name]))
    data = list(dict.fromkeys(data))  # remove duplicate
    return data


def convertFASTAtoSDF(list_file):
    fromFolder = './splitFASTA/'
    resultFolder = './convertFASTAtoSDF/'
    removeAllInFolder(resultFolder)
    for x in list_file:
        obConversion = openbabel.OBConversion()
        obConversion.SetInAndOutFormats("fasta", "sdf")

        obConversion.OpenInAndOutFiles(
            fromFolder + x + '.fasta', resultFolder + x + '.sdf')
        obConversion.Convert()
        obConversion.CloseOutFile()


allDrugs = getColumnData('all_extracted.csv', 'Drug IDs')
allSDF = getColumnData('AllSDF_extracted.csv', 'AllSDF')
allFASTA = getColumnData('AllFASTA_extracted.csv', 'AllFASTA')

drugNotInSDF = []
for drug in allDrugs:
    if drug not in allSDF:
        drugNotInSDF = drugNotInSDF + [drug]

print("Drug not in SDF: ", len(drugNotInSDF))

drugInFasta = []
for drug in drugNotInSDF:
    if drug in allFASTA:
        drugInFasta = drugInFasta + [drug]

print("Drug not in SDF but In Fasta: ", len(drugInFasta))

print("Drug not in SDF and not in FASTA: ",
      len(drugNotInSDF) - len(drugInFasta))

convertFASTAtoSDF(drugInFasta)


# conda install -c conda-forge openbabel
