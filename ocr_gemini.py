#!/usr/bin/env python3
"""
OCR script using Google Gemini API
Extracts text and data from images using Gemini's vision capabilities
"""

import os
import sys
import json
import argparse
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

def setup_gemini(api_key=None):
    """Configure Gemini API with API key"""
    load_dotenv()  # Load environment variables from .env
    if api_key is None:
        api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
            "or pass it as an argument."
        )
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def perform_ocr(image_path, api_key=None, prompt="Extract all text and data from this image. Return the text in a structured format."):
    """
    Perform OCR on an image using Gemini API
    
    Args:
        image_path: Path to the image file
        api_key: Optional Gemini API key (if not provided, uses GEMINI_API_KEY env var)
        prompt: Custom prompt for OCR extraction
    
    Returns:
        Extracted text/data from the image
    """
    try:
        # Load the image
        image = Image.open(image_path)
        
        # Initialize Gemini model
        model = setup_gemini(api_key)
        
        # Perform OCR
        print(f"[📸 perform_ocr] Processing image: {image_path}")
        response = model.generate_content([prompt, image])
        
        # Extract and return the text
        result = response.text
        print(f"[✅ perform_ocr] OCR completed successfully")
        
        return result
    
    except FileNotFoundError:
        print(f"[❌ perform_ocr] Error: Image file not found: {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"[❌ perform_ocr] Error: {str(e)}")
        sys.exit(1)

def main():
    """Main function to run OCR for all JPGs in a specified directory"""
    parser = argparse.ArgumentParser(
        description="Run OCR on all JPGs in a directory using Google Gemini and write results to a file."
    )
    parser.add_argument("images_directory", help="Directory containing images to OCR")
    # Backward compatible positional API key (optional)
    parser.add_argument("api_key", nargs="?", default=None, help="Optional Gemini API key")
    parser.add_argument(
        "--out",
        dest="out_file",
        default=None,
        help="Output JSON file path (default: <images_directory>/ocr_results.json)",
    )
    args = parser.parse_args()

    images_directory = args.images_directory
    api_key = args.api_key
    out_file = args.out_file or os.path.join(images_directory, "ocr_results.json")

    if not os.path.isdir(images_directory):
        print(f"[❌ main] Error: Directory not found: {images_directory}")
        sys.exit(1)

    print(f"[📂 main] Processing images in directory: {images_directory}")
    
    all_results = {}
    for filename in sorted(os.listdir(images_directory)):
        if filename.lower().endswith((".jpg", ".jpeg")):
            image_path = os.path.join(images_directory, filename)
            print(f"\n" + "~"*60)
            print(f"Processing file: {filename}")
            print("~"*60)
            
            result = perform_ocr(image_path, api_key=api_key)
            all_results[filename] = result
            
            print("\n" + "="*60)
            print(f"OCR RESULTS for {filename}:")
            print("="*60)
            print(result)
            print("="*60)

    out_dir = os.path.dirname(out_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"[💾 main] Wrote OCR results to: {out_file}")

    return all_results

if __name__ == "__main__":
    main()

