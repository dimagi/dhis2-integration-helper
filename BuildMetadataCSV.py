#coding=utf-8

import os
import json
import time
import unicodecsv as csv
import datetime

JSON_FOLDER = "Metadata_JSON"
CATEGORYCOMBO_FILENAME = "CategoryCombo"
CATEGORYOPTIONCOMBO_FILENAME = "CategoryOptionCombo"
DATAELEMENT_FILENAME = "DataElement"
DATASET_FILENAME = "DataSet"
ORGUNIT_FILENAME = "OrgUnit"
ORGUNITLEVEL_FILENAME = "OrgUnitLevel"
DATASET_M_DATAELEMENT_FILENAME = "DataSet_m_DataElement"
DATASET_M_ORGUNIT_FILENAME = "DataSet_m_OrgUnit"


def main():
    global JSON_FOLDER
    global CATEGORYCOMBO_FILENAME
    global CATEGORYOPTIONCOMBO_FILENAME
    global DATAELEMENT_FILENAME
    global DATASET_FILENAME
    global ORGUNIT_FILENAME
    global ORGUNITLEVEL_FILENAME

    jsonFolder = JSON_FOLDER
    csvFolder = "Metadata_CSV_{0}".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.mkdir(csvFolder)

    ## Build CategoryComboCSV
    print("Building Category Combo File")
    with open(os.path.join(jsonFolder, "{0}.json".format(CATEGORYCOMBO_FILENAME)), "rb") as categoryComboFile:
        categoryComboDict = json.load(categoryComboFile)
        with open(os.path.join(csvFolder,"{0}.csv".format(CATEGORYCOMBO_FILENAME)), "wb") as csvFile:
            myWriter = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["categoryCombo_id","categoryCombo_name", "dataDimensionType"])
            myWriter.writeheader()
            for categoryCombo in categoryComboDict["categoryCombos"]:
                writeDict = {"categoryCombo_id": categoryCombo["id"], "categoryCombo_name" : categoryCombo["name"], "dataDimensionType": categoryCombo["dataDimensionType"]}
                myWriter.writerow(writeDict)

    ## Build CategoryOptionComboCSV
    print("Building Category Option Combo File")
    with open(os.path.join(jsonFolder, "{0}.json".format(CATEGORYOPTIONCOMBO_FILENAME)), "rb") as categoryOptionComboFile:
        categoryOptionComboDict = json.load(categoryOptionComboFile)
        with open(os.path.join(csvFolder, "{0}.csv".format(CATEGORYOPTIONCOMBO_FILENAME)), "wb") as csvFile:
            myWriter = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["categoryOptionCombo_id","categoryOptionCombo_name", "categoryCombo_id"])
            myWriter.writeheader()
            for categoryOptionCombo in categoryOptionComboDict["categoryOptionCombos"]:
                writeDict = {"categoryOptionCombo_id": categoryOptionCombo["id"], "categoryOptionCombo_name" : categoryOptionCombo["name"], "categoryCombo_id": categoryOptionCombo["categoryCombo"]["id"]}
                myWriter.writerow(writeDict)

    ## Build DataElementCSV
    print("Building Data Element File")
    with open(os.path.join(jsonFolder,"{0}.json".format(DATAELEMENT_FILENAME)), "rb") as dataElementFile:
        dataElementDict = json.load(dataElementFile)
        with open(os.path.join(csvFolder,"{0}.csv".format(DATAELEMENT_FILENAME)), "wb") as csvFile:
            myWriter = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["dataElement_id","dataElement_name", "categoryCombo_id", "valueType"])
            myWriter.writeheader()
            for dataElement in dataElementDict["dataElements"]:
                writeDict = {"dataElement_id": dataElement["id"], "dataElement_name" : dataElement["name"], "categoryCombo_id": dataElement["categoryCombo"]["id"], "valueType": dataElement["valueType"]}
                myWriter.writerow(writeDict)

    ## Build DataSetCSV and DataSet_m_DataElementCSV and DataSet_m_OrgUnitCSV
    print("Building Data Set, DataSet_m_DataElement, and DataSet_m_OrgUnit Files")
    with open(os.path.join(csvFolder,"{0}.csv".format(DATASET_FILENAME)), "wb") as csvDatasetFile:
        with open(os.path.join(csvFolder,"{0}.csv".format(csvFolder, DATASET_M_DATAELEMENT_FILENAME)), "wb") as csvMappingFile:
            with open(os.path.join(csvFolder,"{0}.csv".format(DATASET_M_ORGUNIT_FILENAME)), "wb") as csvOrgUnitMappingFile:
                dataSetWriter = csv.DictWriter(csvDatasetFile, delimiter = ",", fieldnames = ["dataSet_id","dataSet_name", "categoryCombo_id"])
                mappingWriter = csv.DictWriter(csvMappingFile, delimiter = ",", fieldnames = ["dataSet_id", "dataElement_id"])
                orgUnitMappingWriter = csv.DictWriter(csvOrgUnitMappingFile, delimiter = ",", fieldnames = ["dataSet_id", "orgUnit_id"])
                dataSetWriter.writeheader()
                mappingWriter.writeheader()
                orgUnitMappingWriter.writeheader()
                with open(os.path.join(jsonFolder, "{0}.json".format(DATASET_FILENAME)), "rb") as dataSetFile:
                    dataSetDict = json.load(dataSetFile)
                    if "dataSets" not in dataSetDict.keys():
                        dataSetDict = {"dataSets": [dataSetDict]}
                    for dataSet in dataSetDict["dataSets"]:
                        #print(dataSet)
                        dataSetRow = {"dataSet_id": dataSet["id"], "dataSet_name": dataSet["name"], "categoryCombo_id" : dataSet["categoryCombo"]["id"]}
                        dataSetWriter.writerow(dataSetRow)
                        for dataElement in dataSet["dataSetElements"]:
                            mappingRow = {"dataSet_id": dataSet["id"], "dataElement_id" : dataElement["dataElement"]["id"]}
                            mappingWriter.writerow(mappingRow)
                        for orgUnit in dataSet["organisationUnits"]:
                            orgUnitMappingRow = {"dataSet_id": dataSet["id"], "orgUnit_id" : orgUnit["id"]}
                            orgUnitMappingWriter.writerow(orgUnitMappingRow)

    ## Build OrgUnitCSV
    print("Building Org Unit File")
    with open(os.path.join(jsonFolder,"{0}.json".format(ORGUNIT_FILENAME)), "rb") as orgUnitFile:
        orgUnitDict = json.load(orgUnitFile)
        with open(os.path.join(csvFolder,"{0}.csv".format(ORGUNIT_FILENAME)), "wb") as csvFile:
            myWriter = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["orgUnit_id","orgUnit_name", "parent_id","orgUnitLevel"])
            myWriter.writeheader()
            for orgUnit in orgUnitDict["organisationUnits"]:
                writeDict = {"orgUnit_id": orgUnit["id"], "orgUnit_name" : orgUnit["name"], "parent_id": orgUnit["parent"]["id"] if "parent" in orgUnit.keys() else "--", "orgUnitLevel": orgUnit["path"].count("/")}
                myWriter.writerow(writeDict)

    ## Build OrgUnitLevelCSV
    print("Building Org Unit Level File")
    with open(os.path.join(jsonFolder,"{0}.json".format(ORGUNITLEVEL_FILENAME)), "rb") as orgUnitLevelFile:
        orgUnitLevelDict = json.load(orgUnitLevelFile)
        with open(os.path.join(csvFolder,"{0}.csv".format(ORGUNITLEVEL_FILENAME)), "wb") as csvFile:
            myWriter = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["orgUnitLevel_id","orgUnitLevel_name","orgUnitLevel_level"])
            myWriter.writeheader()
            for orgUnitLevel in orgUnitLevelDict["organisationUnitLevels"]:
                writeDict = {"orgUnitLevel_id": orgUnitLevel["id"], "orgUnitLevel_name" : orgUnitLevel["name"], "orgUnitLevel_level": orgUnitLevel["level"]}
                myWriter.writerow(writeDict)

    print("Process complete - CSV files can be found in {0}".format(csvFolder))


if __name__ == "__main__":
    main()