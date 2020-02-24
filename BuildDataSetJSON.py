#coding=utf-8
import requests
import json
import time
import unicodecsv as csv
import datetime
import getpass
import io

username = "admin"
password = "district"

## For a real environment, you'll probably want to prompt the user for password instead of saving it as plaintext
# password = getpass.getpass(prompt="Password: ", stream=None)

myAuth = requests.auth.HTTPBasicAuth(username, password)
dataSetIDList =[]
nextPage = "https://play.dhis2.org/2.31.8/api/29/dataSets.json"
while nextPage is not None:
    r = requests.get(nextPage, auth = myAuth)
    if r.status_code == 200:
        try:
            print(r.text.encode('utf-8'))
            myDict = json.loads(r.text)
            if "nextPage" in myDict["pager"].keys():
                nextPage = myDict["pager"]["nextPage"]
            else:
                nextPage = None
            for dataSet in myDict["dataSets"]:
                dataSetIDList.append(dataSet["id"])
            print(myDict)
            print(nextPage)
            print(dataSetIDList)
        except Exception, e:
            print(str(e))
    else:
        print(r.text)
        print(r.status_code)
        exit()

dataSetList = []

with open("DataSetPullErrorLog.csv", "wb") as csvFile:
    writer = csv.DictWriter(csvFile, delimiter = ",", fieldnames = ["id","displayName","error"])
    writer.writeheader()
    for dataSet_id in dataSetIDList:
        myURL = "https://snigs.gouv.bj/test/api/29/dataSets/{0}/metadata.json".format(dataSet_id)
        r = requests.get(myURL, auth = myAuth)
        if r.status_code == 200:
            myDict = json.loads(r.text.encode("utf-8"))
            if "dataSets" in myDict.keys():
                for dataSet in myDict["dataSets"]:
                    dataSetList.append(dataSet)
            else:
                dataSetList.append(myDict)

        # print(dataSetList)
        # else:
        #     print(r.text.encode("utf-8"))
        #     print(r.status_code)
        #     exit()

with io.open("Metadata_JSON\\DataSet.json", "w", encoding ="utf-8") as dataSetFile:
# with open("DataSet.json", "w") as dataSetFile:
    dataSetJSON = {'dataSets': dataSetList}
    # dataSetJSON = dataSetList
    writeData = json.dumps(dataSetJSON, dataSetFile, ensure_ascii=False)
    dataSetFile.write(unicode(writeData))