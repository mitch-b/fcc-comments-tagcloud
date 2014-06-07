FCC Public Comment Tag Cloud
=====================

View tag cloud of what the public is saying in their FCC comments around net neutrality

#Prerequisites
1. Python 2.7 ([downloads](https://www.python.org/download/releases/2.7.7/))
2. python-pygame Library (available via apt-get, or [binaries here](http://www.pygame.org/download.shtml))
3. pip Python package manager ([instructions](https://pip.pypa.io/en/latest/installing.html))
4. MySQL database instance (community edition [binaries here](http://dev.mysql.com/downloads/mysql/))
5. MySQL Python Connector ([downloads](http://dev.mysql.com/downloads/connector/python/))

#Getting Started

Clone this repository & install Python packages:

```bash
$> git clone https://github.com/mitch-b/fcc-comments-tagcloud.git
$> cd fcc-comments-tagcloud
$> pip install -r requirements.txt     # may require elevated privileges
```

#Configuring MySQL

I know, I know. This will be the point where most of you say, "no, thanks ... I'm out!". I used a database for this project mostly because I had goals of allowing multiple machines to assist collecting all of the data, and building a collective Tag Cloud for all of the United States. This is still possible, but not in its current state. Moving right along now ...

Please follow Oracle's guides on installing MySQL for your system. I've included `mysql.ddl.sql` file which will guide you in creating the database, as well as the table and user scripts. Let's run that script.

```bash
$> mysql -u username -p < mysql.ddl.sql
```

Provide your username above, and it will execute the commands required to host our application. For now, the user has a default password which should get you up and running, but do change this if you plan on hosting this on a machine that is accessed by others.

#How It Works

The way the application works right now, is you provide a City and State via command line, and it will hit an FCC.gov RSS feed of search results, download PDF copies of our public comments, convert the PDF files to text files, then sum up a word count, and use the **pytagcloud** library to build an image which contains the most popular words submitted by citizens of the provided City/State combination.

It is configured to drop the PDFs in a new folder in script directory. Text and image output will drop in a similar fashion.

#Samples
```bash
$> python main.py "Omaha" "NE"
Building tag cloud for Omaha, NE
Populating database with entries...
Entries: 122
Saved: 6017687106
Saved: 6017686902
Saved: 6017686691
Saved: 6017686382
Saved: 6017686094

  .....
  
117 processed records
0 duplicate records
Downloading PDF files...
Downloading item 1
Downloading item 2
Downloading item 3
Downloading item 4
Downloading item 5

  .....
  
Converting PDF files to text...
Parsing PDF 1
Parsing PDF 2
Parsing PDF 3
Parsing PDF 4
Parsing PDF 5

  .....
  
Combining text files and generating tagcloud image...
Finished building tag cloud. It took 84.60283494 seconds to complete.
```

And you will get this nice image output as a result:

####Omaha, NE
![Imgur](http://i.imgur.com/kDCSzN2.png)

####San Francisco, CA
![Imgur](http://i.imgur.com/tqX9Izo.png)

####Chicago, IL
![Imgur](http://i.imgur.com/EqoMXQ0.png)
