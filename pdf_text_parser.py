#! /usr/bin/env python
import sys
import os
import errno
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter


class PdfTextParser:
  city = ''
  state = ''
  pdf_directory = 'pdfs'
  out_directory = 'txts'
  out_file_fmt = 'txt'

  def __init__(self,in_city,in_state):
    self.city = in_city.replace(' ', '')
    self.state = in_state
    self.pdf_directory = 'pdfs/{0}/{1}'.format(self.state,self.city)
    self.out_directory = 'txts/{0}/{1}'.format(self.state,self.city)
    self.init_dl_directory(self.pdf_directory)
    self.init_dl_directory(self.out_directory)

    files = self.get_file_list(self.pdf_directory)
    self.parse(files)


  # http://stackoverflow.com/a/600612
  def init_dl_directory(self, path):
    try:
      os.makedirs(path)
    except OSError as exc:
      if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
      else: raise

  def get_file_list(self, directory):
    return ['{0}/{1}'.format(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]

  def parse(self, files):
    idx = 0
    for file in files:
      id = re.search('\/(\d.*)\.', file).group(1)
      output_filename = '{0}/{1}.{2}'.format(self.out_directory, id, self.out_file_fmt)
      outfp = open(output_filename, 'w')
      outtype = 'text'
      imagewriter=None
      caching=False
      password=''
      maxpages=0
      pagenos = set()
      rotation=0
      # Open a PDF file.
      fp = open(file, 'rb')
      # Create a PDF parser object associated with the file object.
      parser = PDFParser(fp)
      # Create a PDF document object that stores the document structure.
      # Supply the password for initialization.
      try :
        document = PDFDocument(parser, password)
      except Exception as e:
        print 'Failed to open {0} for parsing.'.format(file), e
        continue
      # Check if the document allows text extraction. If not, abort.
      if not document.is_extractable:
          raise PDFTextExtractionNotAllowed
      # Create a PDF resource manager object that stores shared resources.
      rsrcmgr = PDFResourceManager(caching=False)
      # Create a PDF device object.
      device = TextConverter(rsrcmgr, outfp, codec='utf-8',laparams=LAParams(),imagewriter=imagewriter)
      # Create a PDF interpreter object.
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      # Process each page contained in the document.
      for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
      fp.close()
      device.close()
      outfp.close()
      idx += 1
      print 'Parsing PDF', idx

if __name__ == '__main__':
  PdfTextParser()
