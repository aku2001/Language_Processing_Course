import sys
import csv
import json
import re

# Open CSV file
class Converter:

    def __init__(self):
        self.listRegex = re.compile(r'(\w+)\{(\d+|\d+,\d+)\}')
        self.headerRegex = re.compile(r'(\w+\{\d+,\d+\}::\w+|\w+\{\d+\}::\w+|\w+\{\d+,\d+\}|\w+\{\d+\}|\w+,|\w+)')
        self.mediaRegex = re.compile(r'::(\w+)')

    def convert(self, fileName):

        header = []
        rows = []
        jsonArray = []
        i= 0

        file = open(fileName,encoding="utf-8")
        lines = file.readlines()
        header = self.headerRegex.findall(lines.pop(0))
        
        for row in lines:
            row = row.replace("\n",'')
            row = row.split(",")
            
            jsonDict = {}
            for i in range(len(header)):
                if(header[i] != ""):

                    listRes = self.listRegex.search(header[i])
                    atttrList = []
                    
                    if(listRes != None):
                        if(',' in listRes.group(2)):
                            listRange = listRes.group(2).split(",")
                            for j in range(int(listRange[1])):
                                if(row[i+j] != ""):
                                    atttrList.append(row[i+j])
                            

                        
                        else:    
                            for j in range(int(listRes.group(2))):
                                if(row[i+j] != ""):
                                    print(": ",i+j,"attr: ",row[i+j])
                                    atttrList.append(row[i+j])
                            
                            
                        
                        mediaRes = self.mediaRegex.search(header[i])
                        if(mediaRes != None):
                            if(mediaRes.group(1) == "sum"):
                                intList = [int(x) for x in atttrList]
                                sumRes = sum(intList)
                                jsonDict[listRes.group(1)+"_sum"] = sumRes
                            
                            else:
                                print("Wrong Attribute",mediaRes.group(1))

                        else:
                            # Add the list into the dictionary
                            jsonDict[listRes.group(1)] = atttrList
                
                    else:
                        try:
                            jsonDict[header[i]] = row[i]
                        except:
                            pass

            jsonArray.append(jsonDict)

         
        jsonString = json.dumps(jsonArray,indent=4)
        print(jsonString)


if __name__ == "__main__":
    converter = Converter()
    fileName = "C:\\Users\\kutay\\OneDrive\\Masaüstü\\Minho\\Semester_2\\Language Processing\\HW\\TP4\\trial.csv"
    converter.convert(fileName)

    # file = open("trial.csv","r")