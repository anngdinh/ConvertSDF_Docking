import sys
import os
import pandas as pd

import shutil


def getAllSDFname(fileTXT):
    allName = []
    with open(fileTXT, 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            # print (line)
            if line.startswith("> <DATABASE_ID"):
                ne = lines[i + 1][:-1]
                allName.append(str(ne))

    ret_df = pd.DataFrame({"AllSDF": allName})
    ret_file_path = 'AllSDF_extracted.csv'
    ret_df.to_csv(ret_file_path, index=False)
    print(len(allName))
    return allName


def split_3D(allName, location_path, fileTXT):
    indexFile = 0
    close = 1

    file1 = open(fileTXT, 'r', encoding="utf-8")
    try:
        while indexFile < len(allName) + 1:
            line = file1.readline()
            if close == 1:
                if indexFile >= len(allName):
                    break
                # Write file .txt
                file2 = open(
                    location_path + allName[indexFile] + ".txt", "w", encoding="utf-8")

                indexFile = indexFile + 1
                close = 0
            # if line.startswith("DB"): print(line)
            if not line.startswith("$$$$"):
                file2.write(line)
            else:
                file2.write("$$$$")
                file2.close()
                close = 1

                # Convert to sdf file
                thisFile = location_path + allName[indexFile - 1] + ".txt"
                base = os.path.splitext(thisFile)[0]
                os.rename(thisFile, base + ".sdf")

            # if line is empty
            # end of file is reached
            if not line:
                break
    finally:
        file1.close()


def getAllFASTAname(fileTXT):
    allName = []
    with open(fileTXT, 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if line.startswith(">drugbank_drug|"):
                # if '|' in lines[i][15:-1]: print(lines[i][15:22] + '*')
                name = lines[i][15:22]
                # if len(name) > 90:
                #     name = name[:90]
                # name = name.replace("\"", " ")
                # name = name.replace("|", " ")
                # name = name.replace(">", " ")
                # name = name.replace("<", " ")
                # name = name.replace(":", " ")
                # name = name.replace("α", " ")
                allName.append(str(name))

    ret_df = pd.DataFrame({"AllFASTA": allName})
    ret_file_path = 'AllFASTA_extracted.csv'
    ret_df.to_csv(ret_file_path, index=False)
    print(len(allName))
    return allName


def split_FASTA(allName, location_path, fileTXT):
    indexFile = -1
    resultDict = {}
    buff = ""
    file1 = open(fileTXT, 'r', encoding="utf-8")
    try:
        while 1:
            line = file1.readline()
            if line.startswith(">drugbank_drug|"):
                if(indexFile != -1):
                    if allName[indexFile] not in resultDict:
                        resultDict[allName[indexFile]] = buff
                    else:
                        if len(buff) > len(resultDict[allName[indexFile]]):
                            resultDict[allName[indexFile]] = buff
                    
                buff = line
                indexFile = indexFile + 1
            else:
                buff = buff + line
            # if line is empty
            # end of file is reached
            if not line:
                buff = buff + '\n' # for final file 
                if allName[indexFile] not in resultDict:
                    resultDict[allName[indexFile]] = buff
                else:
                    if len(buff) > len(resultDict[allName[indexFile]]):
                        resultDict[allName[indexFile]] = buff
                break
    finally:
        file1.close()
    # print(resultDict)
    for key in resultDict:
        file2 = open(location_path + key + ".txt", "w", encoding="utf-8")
        file2.write(resultDict[key][:-1])
        file2.close()
        
        # Convert to sdf file
        thisFile = location_path + key + ".txt"
        base = os.path.splitext(thisFile)[0]
        os.rename(thisFile, base + ".fasta")


def removeAllInFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\nInvalid arguments, the program accept 1 arguments:\n")
        print("python extract.py <file_name> ")
        print("<file_name> is a big file .sdf or big file .fasta\n")
        print('Example: \npython extract.py \"3D structures_source.sdf\" \npython extract.py \"drug sequences.fasta\" \n')
        sys.exit()

    file_name = sys.argv[1]

    # Convert the copy file from .... to .txt
    base, ext = os.path.splitext(file_name)
    thisFile = base + "-copy" + ext
    shutil.copy2(file_name, thisFile)
    fileTXT = base + "-copy" + ".txt"
    os.rename(thisFile, fileTXT)

    try:
        if ext == '.sdf':
            allName = getAllSDFname(fileTXT)
            # Read big file and split to small file and put in folder  split3D
            location_path = './split3D/'
            removeAllInFolder(location_path)
            split_3D(allName, location_path, fileTXT)
        elif ext == '.fasta':
            allName = getAllFASTAname(fileTXT)
            # Read big file and split to small file and put in folder  splitFASTA
            location_path = './splitFASTA/'
            removeAllInFolder(location_path)
            split_FASTA(allName, location_path, fileTXT)

    finally:
        os.remove(fileTXT)


# python extract.py "3D structures_source.sdf"
# python extract.py "drug sequences.fasta"
