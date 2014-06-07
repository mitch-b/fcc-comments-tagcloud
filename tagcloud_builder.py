#! /usr/bin/env python
import sys
import nltk
import os
import fileinput
import datetime
from operator import itemgetter
from pytagcloud import create_tag_image, make_tags

class TagCloudBuilder:
  city = ''
  state = ''
  wordcount = 100
  txt_directory = ''
  img_directory = 'imgs'
  tagcloud = dict()

  def __init__(self,in_city,in_state):
    self.city = in_city.replace(' ', '')
    self.state = in_state
    self.txt_directory = 'txts/{0}/{1}'.format(self.state,self.city)

    files = self.get_file_list(self.txt_directory)
    self.parse(files)
    self.remove_ignored_words()
    #self.write_to_file()
    self.build_pytag_cloud()

  # StackOverflow
  def get_file_list(self, directory):
    return ['{0}/{1}'.format(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]

  # http://www.mhermans.net/from-pdf-to-wordcloud-using-the-python-nltk.html
  def parse(self, files):
    for file in files:
      f = open(file, 'rU')
      txt = f.read()
      f.close()

      tokens = nltk.word_tokenize(txt) # tokenize text
      clean_tokens = []

      for word in tokens:
        word = word.lower()
        if word.isalpha(): # drop all non-words
          clean_tokens.append(word)

      # make frequency distribution of words
      fd = nltk.FreqDist(clean_tokens)
      for token in fd:
        self.add_to_dictionary(token.lower(), fd[token])

  def add_to_dictionary(self, token, count):
    if token in self.tagcloud:
      self.tagcloud[token] += count
    else:
      self.tagcloud[token]=count

  def remove_ignored_words(self):
    f = open('ignore-words.txt', 'rU')
    for line in f.readlines():
      key = line[:-1] # remove newline
      if key in self.tagcloud:
        del self.tagcloud[key]
    f.close()

  def write_to_file(self):
    f = open('taglist.txt', 'wa')
    f.write(str(self.tagcloud))
    f.close()

  def build_pytag_cloud(self):
    width = 900
    height = 575
    fileName = '{0}/{1}.{2}.{3}.{4}.png'.format(self.img_directory, self.state, self.city, width, height)
    items = sorted(self.tagcloud.iteritems(), key=itemgetter(1), reverse=True)
    tags = make_tags(items[:self.wordcount], maxsize=80)
    create_tag_image(tags, fileName, size=(width, height), fontname='Droid Sans')
    import webbrowser
    webbrowser.open(fileName) # see results

if __name__ == '__main__':
  TagCloudBuilder()
