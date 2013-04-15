import re
import os
import sys
from getpass import *
from mechanize import Browser
from bs4 import BeautifulSoup

"""

This program downloads scpd videos for a given class in the order
that they happened as a wmv, then converts them to a mp4. Each time 
the script is run, it will update to download all of the undownloaded
videos. 

This script is modified from the one by Ben Newhouse (https://github.com/newhouseb).

Unfortunately, there are lots of dependencies to get it up and running
1. Handbrake CLI, for converting to mp4: http://handbrake.fr/downloads2.php
2. BeautifulSoup for parsing: http://www.crummy.com/software/BeautifulSoup/
3. Mechanize for emulating a browser, http://wwwsearch.sourceforge.net/mechanize/

To run:
Change to your username
When prompted, type your password

Usage: python scrape.py "Interactive Computer Graphics"

The way I use it is to keep a folder of videos, and once I have watched them, move them
into a subfolder called watched. So it also wont redowload files that are in a subfolder
called watched.


"""
def _file_exists(file):
	return os.path.isfile(file)

def _first_line_to_back_of_file(list_to_reorder, file):
	course_to_download = list_to_reorder.pop(0)
	f = open(file, 'w')
	f.writelines(list_to_reorder)
	f.write(course_to_download)
	f.close()
	return course_to_download

def _file_to_list(file, no_new_line=False):
	f = open(file, 'r')
	n_list = f.readlines()
	f.close()
	if no_new_line:
		tmp_list = []
		for line in n_list:
			tmp_list.append(_remove_end_newline(line))
		return tmp_list
	return n_list

def _remove_end_newline(line):
	return line.split('\n')[0]

def _append_line_to_file(file, line):
	file_list = _file_to_list(file)
	f = open(file, 'w')
	f.writelines(file_list)
	f.write("%s%s" %(line, '\n'))
	f.close()



def download(work):
  temp = "Not Implemented"
  """
  # work[0] is url, work[1] is wmv, work[2] is mp4
	class_name = re.search('(.*)_', work[2])
	folder_name = "%s/%s" % (current_folder, class_name.group(1))
	
	path_to_vid_mp4 = "%s/%s" % (folder_name, work[2])
	path_to_vid_wmv = "%s/%s" % (folder_name, work[1])
	
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	
	downloaded_videos_path = "%s/%s" % (folder_name, "videos_downloaded.txt")
	
	if not _file_exists(downloaded_videos_path):
		f = open(downloaded_videos_path, 'w')
		f.close()
	
	#import pdb;pdb.set_trace()
	
	downloaded_videos_list = _file_to_list(downloaded_videos_path, no_new_line=True)
	
	global num_vids_already_downloaded
	a = num_vids_already_downloaded
	
	if work[2] in downloaded_videos_list or\
	   work[1] in downloaded_videos_list:
		num_vids_already_downloaded = a + 1
		print "Already downloaded", work[2]
		return
	elif os.path.exists("%s/%s" %(folder_name, work[2])) or\
	     os.path.exists("%s/%s/%s" %(folder_name, "watched", work[2])) or\
	     os.path.exists("%s/%s" %(folder_name, work[1])) or\
	     os.path.exists("%s/%s/%s" %(folder_name, "watched", work[1])):
		num_vids_already_downloaded = a + 1
		_append_line_to_file(downloaded_videos_path, work[2])
		print "Already downloaded", work[2]
		return
	#Comment out this line and uncomment out the other copy of this line
	#_append_line_to_file(downloaded_videos_path, work[2])
	
	print "Starting", path_to_vid_wmv
	
	#This is where the video gets put into the "Videos already Downloading" file
	###Should make this into some sort of method because it's a common operation###
	current_files_downloading_path = "%s/%s" %(current_folder, "current_files_downloading.txt")
	if not _file_exists(current_files_downloading_path):
		f = open(current_files_downloading_path, 'w')
		f.close()
	
	_append_line_to_file(current_files_downloading_path, path_to_vid_wmv)


	os.system("mimms -c %s %s" % (work[0], path_to_vid_wmv))
	convertToMp4(path_to_vid_wmv, path_to_vid_mp4)
	_append_line_to_file(downloaded_videos_path, work[2])
	
	###Need to make a "Remove line from file" function that removes a line from a file###
	#if not _file_exists(current_files_downloading_path):
	#	f = open(current_files_downloading_path, 'w'):
	#	f.close()
	
	
	#import pdb; pdb.set_trace()
	
	new_current_files_downloading_list = []
	current_files_downloading_list = _file_to_list(current_files_downloading_path, no_new_line=True)
	for current_file in current_files_downloading_list:
		if current_file != path_to_vid_wmv:
			new_current_files_downloading_list.append("%s%s" %(current_file,'\n'))
	
	f = open(current_files_downloading_path, 'w')
	f.writelines(new_current_files_downloading_list)
	f.close()
	
	
	print "Finished", path_to_vid_wmv
  """


def begin_scraper():
  br = Browser()
  br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8; rv:16:0) Gecko/20100101 Firefox/16.0')]
  br.set_handle_robots(False)
  br.open("https://wwws.mint.com/login.event")
  assert br.viewing_html()
  formcount=0
  for f in br.forms():
    if str(f.attrs["id"]) == "form-login":
      break
    formcount = formcount+1
  
  br.select_form(nr=formcount)

  br["username"] = "rhintz42@stanford.edu" #Put your username here
  br["password"] = getpass()
  
  
  #import pdb; pdb.set_trace()
  # Submit the user credentials to login to mint 
  response = br.submit()
  response = br.follow_link(text="Transactions")
  links_to_transactions = br.links(text_regex="Export all \d+ transactions")
  link = ""
  for f in links_to_transactions:
    link = f

  response2 = br.follow_link(link)
  text_file = open("transactions.csv", "w")
  text_file.write(response2.read())
  text_file.close()
  #print response.read()

if __name__ == '__main__':
	begin_scraper()
