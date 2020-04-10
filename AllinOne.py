# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:51:27 2020


@author: python MATLAB & GIS
"""
#%%
import datetime
import subprocess
import os
#import sys
import time
from moviepy.editor import VideoFileClip
from pyVideoLib import *
current_dir = os.getcwd()
print(current_dir)

def main():
###########################################
	#overal setup
	
	margin = input('Margin: ')
	silent_threshold_pc = input('silent_threshold percent: ')
	jumpcut_suffix = 'jcmg'+margin+'_'+silent_threshold_pc+'pc'
	
	##########################################################
	#Download using youtube-dl
	# f = 22
	# inList = 'https://www.youtube.com/playlist?list=PL0Fi7QPYOUT_bneUapWqIe7HevHML8thy'
	# youtubedl_pyrun(inList,f)
	
	#rename
	
	duration_sec = 1500
	#	duration_sec = 30
	short_suffix = '_short_'
	long_suffix = '_long_'
	
	datatype_list = ['*.mp4','*.wmv','*.mov','*.avi','*.mkv']
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			rename_based_on_length(inFile, duration_sec,short_suffix,long_suffix)
	
	#######################
	#Convert to mp4
	#	wmv2mp4_yn = input('Do u want to convert all *.wmv to mp4 files? (Y/N)')
	wmv2mp4_yn = 'Y'
	#	mp4_convert_yn = input('Do u want to process converted mp4:(Y/N)')
	mp4_convert_yn = 'N'
	if wmv2mp4_yn.upper() == 'Y':
		for data_type in datatype_list:
			for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
				if data_type != datatype_list[0]:
					f_name,f_ext = os.path.splitext(inFile)
					if mp4_convert_yn.upper() == 'Y':
						outFile = f_name +'.mp4'
						if not os.path.exists(outFile):
							try: 
								ffmpeg_wmv2mp4(inFile,outFile)
							except:
								print(f'ffmpeg_wmv2mp4 is not working with: in: {inFile} out: {outFile} ')
								pass
						if os.path.exists(outFile): print(f'outFile {outFile} is existed')
					else:
						outFile = f_name +'_convert_'+'.mp4'
						if not os.path.exists(outFile):
							try: 
								ffmpeg_wmv2mp4(inFile,outFile)
							except:
								print(f'ffmpeg_wmv2mp4 is not working with: in: {inFile} out: {outFile} ')
								pass
						if os.path.exists(outFile): print(f'outFile is existed')
	
	#############################################
	#split
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			if '_jumpcut_merge_' in inFile:
				print(f'This is merged file: {inFile}, do not split it')
			if '_convert_' in inFile:
				print(f'This is converted file: {inFile}, do not split it')
			else:
				split_new(inFile,duration_sec,jumpcut_suffix,short_suffix,long_suffix)
				
	
	
	#############################################
	#jumpcut
	silent_th = int(silent_threshold_pc)/100
	sound_s = 1
	silent_s = 999999
	jumpcut_list = ['*_short_.wmv','*_short_.mp4','*_long__split*.mp4','*_short_.avi','*_short_.mkv','*_short_.mov']
	for data_type in jumpcut_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			f_name,f_ext = os.path.splitext(inFile)
			outFile = f_name+jumpcut_suffix +'.mp4'
			if jumpcut_suffix in inFile:
				print(f'{jumpcut_suffix.upper()} is in {inFile.upper()} so \n\t so it already jumpcutted')
			if os.path.exists(outFile):
				print(f'{outFile.upper()} is already existed,\n\t which is jumpcuted from {inFile.upper()}')
			if short_suffix in inFile or long_suffix in inFile and not os.path.exists(outFile) and not jumpcut_suffix in inFile:
				print(inFile)
				print(outFile)
				JumpCutterUltra_Py(inFile,silent_th,sound_s,silent_s,margin,outFile)
	#############################################
	#merge
	if len(nameList_F_withExt(current_dir,'*_2merge_.txt'))==0:
		print(f'No _2merge_ text file found')
	else:
		for inFile in nameList_F_withExt(current_dir,'*_2merge_.txt'):
			f_name,f_ext = os.path.splitext(inFile)
			f_name = f_name.replace('_2merge_','')
			outFile = f_name+'_jumpcut_merge_'+'.mp4'
			if os.path.exists(outFile):
				print(f'{outFile} is already existed')
			else:
				ffmpeg_merge_py(inFile,outFile)

if __name__ == "__main__":
	main()
