#!/usr/bin/env python3

from multiprocessing import Pool
import requests
import os
from PyPDF2 import PdfFileMerger
import glob


def download_pdf(url, filename):
    """Download a PDF file from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join("data", filename)
    open(path, "wb").write(response.content)


def download_from_second(second):
    first = 2
    base_url = "https://eref.thieme.de/ebooks/pdf/cs_10278468/210930109"
    for third in range(1, 30):
        print(f"Downloading {first} {second} {third}")
        filename = f"{first:03}_{second:03}_{third:03}.pdf"
        url = f"{base_url}_{filename}"
        print(url)
        try:
            download_pdf(url, filename)
        except requests.exceptions.HTTPError:
            break


def merge_pdfs():
    pdfs = glob.glob(os.path.join("data", "*.pdf"))
    pdfs.sort()
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("Physiologie.pdf")
    merger.close()


if __name__ == "__main__":
    with Pool(20) as pool:
        pool.map(download_from_second, range(1, 30))
    merge_pdfs()
