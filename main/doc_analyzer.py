"""
Document analyzer
by @djangoner
"""
import os
from preview_generator.manager import PreviewManager
from PyPDF2 import PdfFileReader

tmp_path   = '/tmp/preview_cache'
previews_path = 'media/previews'

manager_tmp     = PreviewManager(tmp_path, create_folder= True)
manager_preview = PreviewManager(previews_path, create_folder=True)

def doc_analyzer(file_path):
    pdf_converted = manager_tmp.get_pdf_preview(file_path) # Convert document to PDF and get file path
    pdf_reader    = PdfFileReader(pdf_converted) # Open PDF file with reader
    pages_count   = pdf_reader.pages.lengthFunction() # Extract pages count

    jpg_preview   = manager_preview.get_jpeg_preview(pdf_converted, width=1000, height=1000, page=0) # Generate JPG preview for document

    os.remove(pdf_converted) # Remove temp pdf file
    return {"jpg": jpg_preview, "pages": pages_count}
