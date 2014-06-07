#! /usr/bin/env python
import sys
import time

from comment_import import FccCommentImporter
from pdf_downloader import CommentPdfDownloader
from pdf_text_parser import PdfTextParser
from tagcloud_builder import TagCloudBuilder

city = sys.argv[1]
state = sys.argv[2]
proceeding_id = '14-28'

print 'Building tag cloud for {0}, {1}'.format(city, state)

start = time.time()

print 'Populating database with entries...'
db_prepare = FccCommentImporter(in_city=city,in_state=state,proceeding=proceeding_id)
print 'Downloading PDF files...'
downloader = CommentPdfDownloader(in_city=city,in_state=state)
print 'Converting PDF files to text...'
textParser = PdfTextParser(in_city=city,in_state=state)
print 'Combining text files and generating tagcloud image...'
tagBuilder = TagCloudBuilder(in_city=city,in_state=state)

elapsed = time.time() - start
print 'Finished building tag cloud. It took {0} seconds to complete.'.format(elapsed)
print ''