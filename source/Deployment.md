# [SBI - Identification & Optical character recognition (OCR) for Structured Documents](https://www.techgig.com/hackathon/optical-character-recognition)

## Scope of Work of the PoC

The POC curently is restricted to handling only 
    
    - AI Services to classify different documents using Hashing and Azure Form Recognizers
    - Cognitive Services to extract structured and unstructured text from the documents(Azure Computer Vision OCR)
    - Custom Processor Models for each document type trained to extract required entities (Azure Form Recognizer)
    - Signature Identification using custom model and azure form recognizers
    - Azure Functions for parallel processing of videos and scaling
    - Custom model(RetinaFace) to extract face and Azure Face Detection 
    - Masking of text from KYC documents
    - Azure Containers to store documents/images


Features - 

    1. Image document Classification
    2. Extract structured and unstructured text
    3. Extract required entities
    4. Signature Identification
    5. Face Detection 
    6. Masking of text from KYC documents
    7. The model cuurenlty identifies 42 documents including KYC's and different sbi forms. One can find the documents [here](./data/document_classes/) and the labels json [here](./scripts/document_lables.json)

Post POC Work - 

    1. Train Form Recognizers on large dataset for all possible document type using a combination of empty and handwritten forms and composing them into a single model for classification and extraction.
    2. Train Custom Form Recognizers on KYC documnets that needs to be identified.
    3. Creating a Azure Pipeline to read data in batches from containers, processing them at scale in parallel using Azure functions and storing the ouput json into DB.

## Pre-requisites from the Bank’s side
1. Azure Account
2. Works with both CPU and GPU
3. Setup & Deployment will not require more than a week.
4. Training new models with good data and Pipeline creation cna take somewhere between 8-10 weeks.

## Infrastructure required for setting up the PoC. 
1. The Images can be uploaded to a container storage.
2. An Azure function to deploy this code and call it using REST API's.
3. Azure Form Recognizers 
4. Azure Face Detection 


## Setting up the PoC infrastructure on Microsoft Azure cloud setup
1. [Creating a resource Group](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal#create-resource-groups)
2. [Creating a storage account](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)
3. [Creating a container](https://docs.microsoft.com/en-us/azure/storage/blobs/blob-containers-cli#create-a-container)
4. [Creating a function app](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal#create-a-function-app)
5. [Deploy code in azure function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal#create-function)
6. [Writing scipts to download and upload images to the azure function for processing in azure](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=environment-variable-windows#upload-blobs-to-a-container)
7. [Creating a Form Recognizer Resource](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/create-a-form-recognizer-resource)
8. [Training Custom Models in Form Recognizers](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/concept-custom)
9. [Compsing N custom models into 1 model](https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/compose-custom-models-preview?tabs=studio)
10. [Creating a Face Detection Resource](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts-sdk/identity-client-library?tabs=visual-studio&pivots=programming-language-python)


## High level PoC Key Performance Indicators (KPIs) 
- Samples Processed are provide in the [sample_data](./data/sample_data/) directory and Video of execution can be found [here](https://drive.google.com/file/d/17X2PmlXpnX66G--XUiuAVBTCv2dOL_c-/view?usp=sharing) 

- I have trained around 10 different documents ( 6 Forms and 4 KYCs ) and composed them into one model for use due to cost constraints. This can be scaled up with differenmt form types.

- The Form Recognnizer Models Enity confidence score can be found [here](./data/SBI.json). 

- For Example Entities Trained & Extracted from PAN CARD Form Recognizer Models
    ```"dob": 0.995,
        "father_name": 0.995,
        "name": 0.995,
        "pan_no": 0.995,
        "signature": 0.857
    ```

- Each KYC model captures everything required but the form models are tarined to capture few infomration as name,account no, signatures , dob etc for this POC.

- Document classification is easier if used composed model trained on Azure Form recognizzer, but due to cost only 10 models were trained on it but a hashing based logic for classification is also implemented which can either be removed in Production or enriched with more samples. A hashing directory was craeted using each form and then its used to compare with new forms.

- Face Detection For Images were done using - AZURE FACE DETECTION and Face Detection For PDFs were done using a custom local model [RetinaFace](https://github.com/serengil/retinaface) since calling Azure API for n no of pages would be costly in long run. 

- Signature Validation For Images were doen suing - AZURE FORM RECOGNIZERS and for PDF's it was done using a custom local model [signature-detect
](https://github.com/EnzoSeason/signature_detection) since calling the Azure model for n pages as images would be costly.

- Using the bounding boxes identified by azure form recogniser masking is implemented for KYC documents.

## Deployment Guide
Local Deployment
1. [Ghostscript](https://www.ghostscript.com/doc/current/Install.htm)
2. [Poppler](https://poppler.freedesktop.org/)
3. [Imagewick](https://imagemagick.org/script/download.php)
4. [Python](https://www.python.org/downloads/release/python-390/)
4. First Run will install all the required custom models being used.
5. The Credentails and keys provided with this POC will be avilable till the challenge duration

```cmd
pip3 install vitualenv
virtualenv img_ocr
source img_ocr/bin/activate   
pip3 install -r requirements.txt
python process.py
```