#! /usr/bin/env python
import sys
import mysql.connector
import urllib2
import shutil
import urlparse
import os
import errno

class CommentPdfDownloader:
  city = ''
  state = ''
  download_path = ''
  force_download=False

  def __init__(self, in_city, in_state, force=False):
    self.city = in_city.replace(' ', '')
    self.state = in_state
    self.force_download=force
    self.download_path = 'pdfs/{0}/{1}'.format(self.state,self.city)
    self.init_dl_directory(self.download_path)


    cnx = mysql.connector.connect(user='fccwebuser', password='changeit', database='fcc_comments')
    cursor = cnx.cursor()

    query = ("SELECT id, link FROM `fcc_comments`.`comments`"
             "WHERE city = %s AND state = %s")
    selection = (in_city, self.state)
    cursor.execute(query, selection)
    idx = 1
    for (id, link) in cursor:
      fileName = '{0}/{1}.pdf'.format(self.download_path, id)
      print 'Downloading item', idx
      self.download(link, fileName)
      idx+=1

  # http://stackoverflow.com/a/600612
  def init_dl_directory(self, path):
    try:
      os.makedirs(path)
    except OSError as exc:
      if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
      else: raise

  # stolen from someone online ... source?
  def download(self, url, fileName=None):
    if os.path.isfile(fileName) and not self.force_download:
      print 'skipping (already downloaded)'
      return
    def getFileName(url,openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])
    try:
      r = urllib2.urlopen(urllib2.Request(url))
    except Exception as err:
      print 'Download failed > ', url
      return
    try:
        fileName = fileName or getFileName(url,r)
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r,f)
    finally:
        r.close()

if __name__ == '__main__':
  CommentPdfDownloader()
