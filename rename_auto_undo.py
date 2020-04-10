# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:51:27 2020

@author: python MATLAB & GIS
"""
import datetime
import subprocess
import os
import sys
import time
from moviepy.editor import VideoFileClip
current_dir = os.getcwd()
print(current_dir)

#%%
def main():

	duration_sec = 1500
	short_suffix = '_short_'
	long_suffix = '_long_'
	datatype_list = ['*.mp4','*.wmv','*.mov','*.avi']
	for data_type in datatype_list:
		rename_undo2(current_dir,data_type)
#%%
def rename_undo2(InputFolder,data_type='*.mp4'):
	short_suffix = '_short_'
	long_suffix = '_long_'
	for file in nameList_F_withExt(InputFolder,data_type):
		long_name = file
		short_name = long_name.replace('_long_','')
		short_name = short_name.replace('_long_','')
		short_name = short_name.replace('_long_','')
		short_name = short_name.replace('_short_','')
		short_name = short_name.replace('_short_','')
		short_name = short_name.replace('_short_','')
		print(f'{long_name} == > {short_name}')
		if '_split' in long_name:
			print('This is a splitted video, you can not redo the name')
			pass
		else:
			try: os.rename(long_name, short_name)
			except Exception as error:
				print(error)
				pass

def rename_undo(rename_auto_file):
	undo_info = open(rename_auto_file,'r')
	for line in undo_info:
		words = line.split(',')
		old_name = words[0]
		old_name = old_name. rstrip()
		new_name = words[1]
		new_name = new_name. rstrip()
		print(new_name)
		print(old_name)
		os.rename(new_name, old_name)
	undo_info.close()
	print(100*'#'+'\n')
#remove the file
	os.remove(rename_auto_file)



def clip_duration(invideoF):
	clip = VideoFileClip(invideoF)
	clip_duration = clip.duration
	clip.close()
	return clip_duration


#print(clip_duration('0_20120829_matlab_ValSchmidt_split1_cut1.mp4','hms'))
#print(clip_duration('0_20120829_matlab_ValSchmidt_split1_cut1.mp4','sec'))


#% time handling functions
def get_sec(time_str):
	"""Get Seconds from time."""
	h, m, s = time_str.split(':')
	return int(h) * 3600 + int(m) * 60 + int(s)
#print(get_sec('00:30:40'))
#print(get_sec('00:04:15'))
#print(get_sec('00:00:25'))


def get_sec_datetime(time_str):
	h,m,s = time_str.split(':')
	return int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())

#print(get_sec_datetime('1:23:45'))


def get_strtime(time_sec):
	return time.strftime('%H:%M:%S', time.gmtime(time_sec))
#get_strtime(5025)


def ffmpeg_split(inFile,outFile,start_point,duration_sec):
	ffmpegFile = "D:/Downloads/youtube-dl/ffmpeg.exe"
	subprocess.call([ffmpegFile,'-i',inFile,'-ss',str(start_point),'-t',str(duration_sec),outFile])
# ffmpeg -i t.mp4 -ss 00:00:00 -t 2440 -c:v h264_nvenc t_split1.mp4

#########################################################################################################
#% list all file with extentions
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
#%%
if __name__ == "__main__":
	main()
