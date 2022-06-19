from PIL import Image
import imagehash
import os
import glob 
import pickle
from extract_image_from_pdf import extract_image
def get_new_hashes():
    hash_dir = {}
    print("INFO : TRAINING STARTED!")
    files = []
    for ext in (glob.glob(f"../data/document_classes/*.jpeg"), glob.glob(f"../data/document_classes/*.png"), glob.glob(f"../data/document_classes/*.jpg")):
        files.extend(ext)
    print("NO OF Classes: ",len(files))
    for path in files:
        try:
            imghash = imagehash.average_hash(Image.open(path))
            hash_dir[path.split(os.sep)[-1].split(".")[0]] = imghash
        except:
            print(path)
    
    print("INFO : HAHSES SAVED!")
    with open('../data/hash_dir.pickle', 'wb') as handle:
        pickle.dump(hash_dir, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(len(hash_dir))
    return "/data/hash_dir.pickle"

def classify_document(image_path,debug):
    with open('../data/hash_dir.pickle', 'rb') as handle:
        hash_dir = pickle.load(handle)
    imghash = imagehash.average_hash(Image.open(image_path))
    min_score = 100000
    match = None
    matches = []
    for key,hash_val in hash_dir.items():
        score = abs(imghash-hash_val)
        matches.append((key,score))
        if score < min_score:
            min_score = score
            match = key
    if debug:
        print(sorted(matches,key = lambda x:x[1]))
    return [match,min_score] # lower is better


def get_classification(path,debug = False):
    if "pdf" not in path.lower():
        result  = classify_document(path,debug)
    else:
        img_path = extract_image(path)
        result  = classify_document(img_path,debug)
    if debug:
        print(result)
    return result

if __name__ == "__main__":
    ## Toggle this to True to get new hashes
    train_new_hases = False
    if train_new_hases:
        saved_path = get_new_hashes()
        print(f"Hashes Created and Saved at: {saved_path}")