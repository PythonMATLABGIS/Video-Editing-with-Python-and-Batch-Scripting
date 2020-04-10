# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:51:27 2020

@author: python MATLAB & GIS
"""
import datetime
import subprocess
import os
import time
from moviepy.editor import VideoFileClip
current_dir = os.getcwd()
print(current_dir)


def main():
	out_ffmpeg_merge_txtf = open('merge_list.txt','w')	
	for idx,inFile in enumerate(nameList_F_withExt(current_dir,'*_jcmg1.mp4')):
		in_name,in_ext = os.path.splitext(inFile)
		msg = 'file ' + "'" + inFile + "'"
		out_ffmpeg_merge_txtf.write(msg+'\n')
		
	out_ffmpeg_merge_txtf.close()


#########################################################################################################
#%% list all file with extentions
def nameList_F_withExt(InputFolder,filterString="*"):
	'''
	pathList_F_ext(InputFolder,filterString="*")
	list all files and folders in InputFolder
	return a list of names for every file and folder matching folderString
	file includes extention (ext) information
	'''	
	
	import glob	
	os.chdir(InputFolder) #change working folder
	return glob.glob(filterString)

if __name__ == "__main__": 
	main()
