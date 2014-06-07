#! /usr/bin/env python
import feedparser
import mysql.connector
import urllib
import sys
import os
import re

class FccCommentImporter:
  proceeding_id = ''
  proceeding_pattern = 'Proceeding:\s(.*?)\s'
  id_pattern = 'id=(.*)'
  pdf_pattern = '(http:\/\/apps.fcc.gov\/ecfs\/document\/view\?id=.*?)"'
  successes = 0
  duplicates = 0

  def __init__(self, in_city, in_state, proceeding):
    global rssUrl
    global state
    global city
    global cnx
    global cursor

    cnx = mysql.connector.connect(user='fccwebuser', password='changeit', database='fcc_comments')
    cursor = cnx.cursor()

    self.proceeding_id = proceeding
    state = in_state
    city = urllib.quote(in_city,'') # deal with spaces in names

    rssUrl = 'http://apps.fcc.gov/ecfs/comment_search/rss?recieved.minDate=6%2F5%2F13&address.state.stateCd={0}&address.city={1}'.format(state,city)
    self.load_from_rss(rssUrl)
    if rss:
      self.loop()
    else:
      print 'No entries found.'
      sys.exit(0)

    cnx.commit()
    cursor.close()
    cnx.close()
    print self.successes, 'processed records'
    print self.duplicates, 'duplicate records'

  def load_from_rss(self, url):
    global rss
    rss = feedparser.parse(url)
    print "Entries:", len(rss['entries'])

  def loop(self):
    for post in rss.entries:

      # selection criteria of comments
      proceeding = re.search(self.proceeding_pattern, post.description)
      if proceeding is None: # this comment is not related to net neutrality
        continue
      if proceeding.group(1) != self.proceeding_id:
        continue
      rval = re.search(self.id_pattern, post.id)
      if rval is None:
        continue
      url = re.search(self.pdf_pattern, post.description)
      if url is None:
        continue

      # logical naming for data
      post_id = rval.group(1)
      link = url.group(1)

      # prepare MySQL query
      add_post = ("INSERT INTO comments "
        "(id, name, date_submitted, link, proceeding, state, city) "
        "VALUES (%s, %s,%s,%s,%s, %s, %s)")
      post_data = (post_id, post.author, post.date, link, self.proceeding_id, state, urllib.unquote(city))

      try:
        cursor.execute(add_post, post_data)
        print 'Saved:', post_id
        self.successes += 1
      except mysql.connector.IntegrityError as err:
        print 'Integrity violation:', post_id
        self.duplicates += 1
      except Exception as e:
        print 'Failed to insert record:', e

if __name__ == "__main__":
  FccCommentImporter()
