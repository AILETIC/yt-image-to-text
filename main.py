import tqdm 
import os
import pytesseract
import json
import img2pdf
import cv2

# -----------------------
# easy functions
# -----------------------

def get_pages_easy(
        DIR:str, 
        file_type:str = "JPG"
    ) -> list:

    """ returns a list of file paths from a certain directory """

    pages = []
    for path in os.listdir(DIR):
        if path[-len(file_type):] == file_type:
            pages.append(DIR + path)

    pages = sorted(pages)
    return pages

def get_images_easy(
        pages:list
    ) -> list:
    """ returns a list of ndarray (images, rgb) """
    images = []
    for path in pages:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)
    return images

def get_text_from_images_easy(
        images, 
        language="eng", 
        config="--psm 6"
    ) -> dict:

    """ 
        returns a dictonary, containing a list of pages 
        with there respective text 

        Page segmentation modes:
        0    Orientation and script detection (OSD) only.
        1    Automatic page segmentation with OSD.
        2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
        3    Fully automatic page segmentation, but no OSD. (Default)
        4    Assume a single column of text of variable sizes.
        5    Assume a single uniform block of vertically aligned text.
        6    Assume a single uniform block of text.
        7    Treat the image as a single text line.
        8    Treat the image as a single word.
        9    Treat the image as a single word in a circle.
        10    Treat the image as a single character.
        11    Sparse text. Find as much text as possible in no particular order.
        12    Sparse text with OSD.
        13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
        
    """

    data = {
        "pages": []
    }

    for image in tqdm.tqdm(images):
        text = pytesseract.image_to_string(
            image, 
            lang=language, 
            config=config
        )
        data["pages"].append(text)

    return data

# --------------------------
# list / dict comprehensions
# --------------------------

def get_pages(
        DIR:str, 
        file_type:str = "jpg"
    ) -> list:

    """ returns a list of file paths from a certain directory """

    return sorted([
        DIR + elem 
        for elem 
        in os.listdir(DIR) 
        if elem[-len(file_type):] == file_type
    ])

def get_images(
        pages:list
    ) -> list:
    """ returns a list of ndarray (images, rgb) """
    return [
        cv2.cvtColor(
            cv2.imread(elem), 
            cv2.COLOR_BGR2RGB
        ) 
        for elem in pages
    ]

def get_text_from_images(
        images,
        language="eng",
        config="--psm 6"
    ) -> dict:

    """ 
        returns a dictonary, containing a list of pages with 
        there respective text
    """
    return {
        "pages": [
            pytesseract.image_to_string(
                image, 
                lang=language, 
                config=config
            ) 
            for image 
            in tqdm.tqdm(images)
        ]
    }

def save_text(
        data:dict,
        filename:str = "output",
        type:str ="txt"
    ) -> None:

    """ 
        saves the extracted text either as a whole as 
        text file or as json as dictonary 
    """

    if type == "txt":
        with open(filename + ".txt", "w") as fp:
            fp.write("".join(data["pages"]))
    elif type == "json":
        with open(filename + ".json", "w") as fp:
            json.dump(data, fp)
    else:
        print("warning: not the correct file type, \
              choose between 'txt' and 'json'")

def save_pdf(
        images:list,
        filename:str = "output"
    ) -> None:

    """ saves images as pdf """

    pdf_data = img2pdf.convert(images)

    with open(filename + ".pdf", "wb") as file:
        file.write(pdf_data)

def main():
    DIR = "pages/"

    # get img file paths
    pages = get_pages(DIR)

    # get book pages as images
    images = get_images(pages)
    
    # get text and data from images (data -> dict)
    data = get_text_from_images(
        images, 
        language="eng"
    )

    # saves as text and as pdf
    save_text(data, type="txt")
    save_pdf(pages)

if __name__ == "__main__":
    main()