from pdf2image import convert_from_path
import os
import argparse
import subprocess
from loguru import logger


def perform_ocr(image_paths, ocr_output_folder):
    if not os.path.exists(ocr_output_folder):
        os.makedirs(ocr_output_folder)

    os_env = os.environ.copy()
    for image_path in image_paths:
        base_name = os.path.basename(image_path)
        txt_output_path = os.path.join(ocr_output_folder, base_name + ".txt")

        # Run tesseract OCR on the image
        tesseract_comma = f"tesseract -l chi_sim --psm 6 {image_path} {txt_output_path.rstrip('.txt')}"
        logger.info(f"Runing command: {tesseract_comma}")
        process = subprocess.run(tesseract_comma, shell=True, env=os_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", process.stdout)
        print("STDERR:", process.stderr)


def combine_txt_files(ocr_output_folder, combined_output_path):
    with open(combined_output_path, "w") as outfile:
        for filename in os.listdir(ocr_output_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(ocr_output_folder, filename), "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Optionally, add a newline between texts


def convert_pdf_to_images(pdf_path, output_folder):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    raw_img_folder = os.path.join(output_folder, "raw_images")
    if not os.path.exists(raw_img_folder):
        os.makedirs(raw_img_folder)

    # Save each image in the output folder
    images_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(raw_img_folder, f"page_{i + 1}.png")
        images_paths.append(image_path)
        image.save(image_path, "PNG")
        print(f"Saved page {i + 1} as {image_path}")

    return images_paths


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Convert a PDF file to a sequence of images")

    # Add arguments for the PDF path and the output folder
    parser.add_argument("--pdf_path", required=True, help="Path to the PDF file")
    parser.add_argument("--output_folder", required=True, help="Path to the output folder where images will be saved")

    # Parse the arguments
    args = parser.parse_args()

    print(f"PDF Path: {args.pdf_path}")
    print(f"Output Folder: {args.output_folder}")
    # Convert the PDF to images
    image_paths = convert_pdf_to_images(args.pdf_path, args.output_folder)
    ocr_output_folder = os.path.join(args.output_folder, "ocr_output")
    if not os.path.exists(ocr_output_folder):
        os.makedirs(ocr_output_folder)
    perform_ocr(image_paths, ocr_output_folder)
    combined_output_path = os.path.join(ocr_output_folder, "combined_output.txt")
    combine_txt_files(ocr_output_folder, combined_output_path)
