import cv2
import matplotlib.pyplot as plt
from signature_detect.loader import Loader
from signature_detect.extractor import Extractor
from signature_detect.cropper import Cropper
from signature_detect.judger import Judger


def show_image(img):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(img)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

def detect_signature(path,debug = False):
    image = cv2.imread(path)
    if "pdf" not in path:
        if debug:
            show_image(image)

        loader = Loader()
        mask = loader.get_masks(path)[0]
        if debug:
            show_image(mask)

        extractor = Extractor(amplfier=15)
        labeled_mask = extractor.extract(mask)
        if debug:
            show_image(labeled_mask)

        cropper = Cropper()
        results = cropper.run(labeled_mask)

        if results:
            signature = results[0]["cropped_mask"]
            if debug:
                show_image(signature)
        else:
            signature = None

        judger = Judger()
        result = judger.judge(signature)
        return result
    else:
        loader = Loader()
        extractor = Extractor(amplfier=15)
        cropper = Cropper(border_ratio=0)
        judger = Judger()

        masks = loader.get_masks(path)
        if debug:
            for i in range(len(masks)):
                show_image(masks[i])

        is_signed = False
        for i in range(len(masks)):
            labeled_mask = extractor.extract(masks[i])
            if debug:
                show_image(labeled_mask)
            results = cropper.run(labeled_mask)
            for result in results.values():
                is_signed = judger.judge(result["cropped_mask"])
                if is_signed:
                    if debug:
                        show_image(result["cropped_mask"])
                    break
            if is_signed:
                break
        return is_signed

