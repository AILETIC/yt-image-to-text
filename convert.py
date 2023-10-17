from main import *
import argparse

parser = argparse.ArgumentParser(
    prog='convertPages',
    description='It converts images to txt and pdf.'
)

parser.add_argument('-f', '--filetype', default='jpg')
args = parser.parse_args()

print(args)

def main():
    DIR = "pages/"

    # get img file paths
    pages = get_pages(DIR, file_type=args.filetype)

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