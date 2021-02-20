"""
Pages counter
by @djangoner
{VER}
"""
import os
import zipfile, xml.dom.minidom, sys, getopt
from functools import wraps

REGISTERED_HANDLERS = {}
def register_handler(ext_list):
    "Register document handler"
    def wrapper(f):
        for ext in ext_list:
            REGISTERED_HANDLERS[ext] = f
        ##
        @wraps(f)
        def inner(*args, **kwargs):
            return f(*args, **kwargs)

    return wrapper

def pages_count(file, *args, **kwargs):
    ext = file.split(".")[-1] # Extract extension
    if not ext in REGISTERED_HANDLERS:
        raise RuntimeError("Handler for %s format is not registered!" % ext)

    handler = REGISTERED_HANDLERS[ext]
    # Pass args to handler
    return handler(file, *args, **kwargs)

###

@register_handler(["doc", "docx"])
def parser_docx(file):
    document = zipfile.ZipFile(file)
    dxml = document.read('docProps/app.xml')
    uglyXml = xml.dom.minidom.parseString(dxml)
    pages = uglyXml.getElementsByTagName('Pages')[0].childNodes[0].nodeValue
    return int(pages)
