from classify_document import get_classification
from detect_faces import detect_faces
from form_recognizer import extract_information
from azure_ocr_extraction import extract_information_unknown
from masking_kyc import mask_documents
from signature_detection import detect_signature
from utility import upload_blob,check_signature_from_azure
import json,os

with open('azure_config.json','r') as f:
    config = json.load(f)

with open('document_lables.json','r') as f:
    class_labels = json.load(f)

# no of documents being indentified - 42

detection_threshold = 0.70

def process_document(path):
    try:
        response = {}
        print("INFO : UPLOADING FILE TO AZURE BLOB")
        upload_url = upload_blob(path,config["container_name"],config["connect_str"])
        print("INFO : UPLOADED TO AZURE :",upload_url)
        print()
        print("INFO : CLASSIFYING DOCUMENT - HASHING")
        classification = get_classification(path,debug = False)
        print("INFO : DOCUMENT CLASSIFICTAION :",class_labels.get(classification[0],classification[0]))
        print("INFO : SCORE :",classification[1])
        print()
        print("INFO : DETECTING FACES")
        if 'pdf' in upload_url.lower():
            faces = detect_faces(path,config,debug=False)
        else:
            faces = detect_faces(upload_url,config,debug=False)
        print("INFO : NO OF FACES DETECTED :",len(faces))
        print()
        print("INFO : EXTRACTING DATA FROM THE DOCUMENT UPLOADED!")
        data_extracted = extract_information(upload_url,config)
        if data_extracted['document_detected'] and float(list(data_extracted['document_detected'].values())[0]) <= detection_threshold:
            print("INFO : DOCUMENT NOT TRAINED IN FORM RECOGNIZER USING GENERIC MODEL!")
            data_extracted = extract_information_unknown(upload_url,config)
        else:
            print("INFO : DOCUMENT TRAINED IN FORM RECOGNIZER CHANGING DETECTED DOCUMENT!")
        print("INFO : DATA EXTRACTED :",list(data_extracted.keys()))
        print("INFO : LABELS DETECTED :",data_extracted['identified_labels'])
        print()
        filename = path.split(os.sep)[-1].split(".")[0] + ".json"
        document_classification = list(data_extracted["document_detected"].keys())[0].split(":")[1]  if data_extracted.get("document_detected",None) else classification[0]
        classification_score = list(data_extracted["document_detected"].values())[0]  if data_extracted.get("document_detected",None) else classification[1]
        
        print("INFO : DETECTING SIGNATURE IN THE DOCUMENT UPLOADED!")
        signature_present = detect_signature(path,debug = False)
        print("INFO : SIGNATURE DETECTED FROM LOCAL MODEL :",signature_present)
        signature_present = check_signature_from_azure(data_extracted["identified_labels"],signature_present)
        print("INFO : SIGNATURE DETECTED FROM AZURE :",signature_present)
        print("INFO : SIGNATURE DETECTED FINAL :",signature_present)
        print()
        
        response = {
            "local_path":path,
            "blob_url":upload_url,
            "document_classification":class_labels.get(document_classification,document_classification),
            "classification_score":classification_score,
            "faces_detected":faces,
            "signature_present":signature_present,
            "data_extracted":data_extracted
        }
        print("INFO : DOCUMENT FINAL CLASIFICATION :",response['document_classification'])
        print()

        if response['document_classification'] in ["AADHAAR_CARD","PASSPORT_INDIAN","PAN_CARD","DRIVING_LICENSE_INDIAN"]:
            print("INFO : MASKING KYC IMAGE DATA")
            mask_documents(path,response['document_classification'],data_extracted['labels_coordinates'])
            print("INFO : MASKING DONE")
            print()


        print("INFO : SAVING RESPONSE")
        output_path = os.path.join(f"{os.sep}".join(path.split(os.sep)[:-1]),filename)
        with open(output_path, "w") as f:
            json.dump(response,f,indent=4)
        print("INFO : OUTPUT FILE SAVED AT: ",output_path)
        print("INFO : PROCESS COMPLETED!")
    except Exception as e:
        print("ERROR : ",str(e))

if __name__ == "__main__":  
    path = "../data/sample_data/dl6.jpeg"
    process_document(path)

# Classification - 
#     PDF - "../data/sample_data/link-aadhaar.pdf"
#     Image - "../data/sample_data/pass6.png"

# Face Detection - 
#     PDF - "../data/sample_data/AO-Form.pdf"
#     Image - "../data/sample_data/pan_processed.jpeg"

# Data Extarction - 
#     PDF - "../data/sample_data/ib-reg.pdf"
#     Image - "../data/sample_data/20-nov-sbi-statement.jpeg"

# Signature detection - 
#     PDF - "../data/sample_data/link-aadhaar.pdf"
#     Image - "../data/sample_data/pan_processed.jpeg"

# Masking - 
#     Aadhar - "../data/sample_data/a9.jpeg"
#     DL - "../data/sample_data/dl6.jpeg"