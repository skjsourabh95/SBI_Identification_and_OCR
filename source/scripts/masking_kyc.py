from PIL import Image, ImageDraw
import os

# fields to mask in each KYC 
masking_fields = {
    "AADHAAR_CARD":["dob","aadhaar_no"],
    "PAN_CARD":["dob","pan_no"],
    "PASSPORT_INDIAN":["passport_no","dob","MRZ"],
    "DRIVING_LICENSE_INDIAN":["dl_no","id"]
}

color = (0, 165, 255) #BGR

def mask_documents(path,document_classification,cords):
    mask = Image.open(path)
    draw = ImageDraw.Draw(mask)
    for label in masking_fields[document_classification]:
        (x1, y1, x2, y2) = cords[label]
        draw.rectangle(((x1, y1), (x2, y2)), fill = True)
    
    mask.show()

    filename = f"{path.split(os.sep)[-1].split('.')[0]}-masked.jpeg"
    output_path = os.path.join(f"{os.sep}".join(path.split(os.sep)[:-1]),filename)
    print(output_path)
    if mask.mode in ("RGBA", "P"): 
        mask = mask.convert("RGB")
    mask.save(output_path)
   
