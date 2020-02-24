# dhis2-integration-helper
## Warning
The process outlined here is not officially supported by any division within Dimagi. The process has been used to pull metadata from a limited subset of DHIS2 instances onto a Windows PC. DHIS2 servers differ, and the process may need to be adjusted depending on the specific configuration of your server.

None of the scripts here are designed to be run "out of the box". They are intended more as examples to build your own process.

## Summary
The process outlined here allows you to pull all metadata from a DHIS2 server that is relevant for a Data Set integration. The output of this process is an Excel workbook with mappings from Data Sets to Data Elements, Data Sets to Organisation Units, Data Sets to Category Option Combos, and Data Elements to Category Option Combos. This Excel workbook also contains a tab mapping every possible variation of Data Set, Data Element, and Category Option Combo.

Ultimately, this output should be used to guide your implementation of a Data Set integration, and/or to help guide requirements conversations with a partner.

## Assumptions
This document assumes that the user is comfortable navigating to folders in the command line, and that the user either has Python installed or knows how to download and install Python.

## Contents of Git Repo
The relevant Python scripts, Excel dashboard, and a sample set of JSON files (pulled from [version 2.31.8 of the DHIS2 demo server](https://play.dhis2.org/2.31.8/)) are included in this repository. The contents of the folder are as follows:
- **README.md**
- **BuildMetadataCSV.py** is a Python script used to convert JSON metadata into tabular CSV feils
- **BuildDataSetJSON.py** is a Python script for use in the event that the DHIS2 server in question does not support direct export of Dataset metadata
- **DHIS2_Metadata_Workbook.xlsx** is an Excel workbook containing tabs into which to paste the CSV data generated above. Its final page, DataSet_m_DataElement_DisAgg, contains a disaggregated view that's generated via Excel Queries (this may need to be manually refreshed once data is copied in)
- **Metadata_JSON** is a folder containing sample JSON data from the DHIS2 demo server. You will replace these files with data from your own DHIS2 server. Files include:
-- **CategoryCombo.json**
-- **CategoryOptionCombo.json**
-- **DataElement.json**
-- **DataSet.json**
-- **OrgUnit.json**
-- **OrgUnitLevel.json**

## Using the Contents
- Download the DHIS2 Metadata Script folder IN ITS ENTIRETY to your computer.
- Rename or delete Metadata_JSON folder
- Create new empty Metadata_JSON folder
- Log into the relevant DHIS2 server, and visit the Meta Data Export page (under Import/Export)
-- e.g. [https://play.dhis2.org/2.31.8/dhis-web-importexport/index.html#/export/metadata](https://play.dhis2.org/2.31.8/dhis-web-importexport/index.html#/export/metadata)
- Click "Select None", then check the "Category Combo" box. Specify format = "JSON", compression = "Uncompressed", and click "Export"
- Copy the resulting .json file to Metadata_JSON. Rename it to "CategoryCombo.json"
- Repeat these steps once for each of the following pieces of data (see example files for appropriate naming conventions):
-- CategoryOptionCombo
-- DataElement
-- OrgUnit
-- OrgUnitLevel
-- DataSet
--- If you cannot pull DataSet from your server's metadata export page, modify BuildDataSetJSON.py with a pointer to the correct server location/credentials and run it in the Command Prompt/Terminal to generate DataSet.json
- Once the Metadata_JSON folder has been populated with metadata from your own server, open the Command Prompt (or Terminal in Mac OS or other Unix-like OSes) and navigate to the folder containing BuildMetadataCSV.py. Type the following to run the script:
-- python BuildMetadataCSV.py
- If all goes well, the script should create a new folder containing the following CSV files:
-- CategoryCombo.csv
-- CategoryOptionCombo.csv
-- DataElement.csv
-- DataSet.csv
-- DataSet_m_DataElement.csv
-- DataSet_m_OrgUnit.csv
-- OrgUnit.csv
-- OrgUnitLevel.csv
- Open DHIS2_Metadata_Workbook.xlsx in Excel. Copy the contents of each CSV file generated above into the corresponding tabs in the Excel workbook.
-- **NOTE 1**: Do not alter the column names in any tab of the Workbook
-- **NOTE 2**: Pasting data may result in the existing rows being displaced, so you may need to delete the sample data after pasting
-- **NOTE 3: DO NOT ALTER ANY DATA IN THE DataSet_m_DataElement_DisAgg tab**
- Once all of the tabs have been populated, the DataSet_m_DataElement_DisAgg tab should update automatically. If not, 
-- Navigate to the Data ribbon
-- In the Get & Transform section select Show Queries
-- In the right hand sidebar, right-click DataSet_m_DataElement_DisAgg and select "Refresh"
- If you've followed all of the above steps and all of the planets and constellations have aligned, then congratulations! You can now see every individual DataSet/DataElement/CategoryOptionCombo variation in the DHIS2 data set! From here, feel free to hide, sort and filter data to your heart's content.
