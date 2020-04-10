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
#import time
from datetime import datetime as dt
from moviepy.editor import VideoFileClip
from pyVideoLib import *
current_dir = os.getcwd()
print(100*'#')
print(100*'-')
print(f' Working folder: {current_dir}')
print(50*'-')
def main():
	stime = dt.now()
###########################################
	#overal setup
	print(' General setup:')
#	margin = input('Margin: ')
	margin = 1
#	silent_threshold_pc = input('silent_threshold percent: ')
	silent_threshold_pc = 4
	jumpcut_suffix = 'jcmg'+str(margin)+'_'+str(silent_threshold_pc)+'pc'
	print(f'\t jumpcut_suffix: {jumpcut_suffix}')
	##########################################################
	#Download using youtube-dl
	# f = 22
	# inList = 'https://www.youtube.com/playlist?list=PL0Fi7QPYOUT_bneUapWqIe7HevHML8thy'
	# youtubedl_pyrun(inList,f)
	
	#rename
	print(50*'-')
	print(' Rename setup:')
	duration_sec = 1500
	print(f'\t duration_sec: {duration_sec}')
	#	duration_sec = 30
	short_suffix = '_short_'
	print(f'\t short_suffix: {short_suffix}')
	long_suffix = '_long_'
	print(f'\t long_suffix: {long_suffix}')
	
	datatype_list = ['*.mp4','*.wmv','*.mov','*.avi','*.mkv']
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			rename_based_on_length(inFile, duration_sec,short_suffix,long_suffix)
	
	#######################
	stime_convert = dt.now()
	print(50*'-')
	print(' Convert to mp4 setup:')
	#Convert to mp4
	#	wmv2mp4_yn = input('Do u want to convert all *.wmv to mp4 files? (Y/N)')
	wmv2mp4_yn = 'N'
	print(f'\t wmv2mp4_yn: {wmv2mp4_yn}')
	#	mp4_convert_yn = input('Do u want to process converted mp4:(Y/N)')
	mp4_convert_yn = 'N'
	print(f'\t mp4_convert_yn: {mp4_convert_yn}')
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
	print('\tConverting time: %s' % (dt.now() - stime_convert))
	#############################################
	#split
	stime_split = dt.now()
	print(50*'-')
	print(' Split setup:')
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			print(f'\t inFile: {inFile}')
			if '_jumpcut_merge_' in inFile:
				print(f'This is merged file: {inFile}, do not split it')
			if '_convert_' in inFile:
				print(f'This is converted file: {inFile}, do not split it')
			else:
				print(f'\t split_new is running with infile: {inFile}')
				split_new(inFile,duration_sec,jumpcut_suffix,short_suffix,long_suffix)
				
	print('\tSplitting time: %s' % (dt.now() - stime_split))
	
	#############################################
	#jumpcut
	stime_jc = dt.now()
	print(50*'-')
	print(' JumpCutter setup:')
	print(f'\tMargin: {margin}')
	print(f'\tsilent_threshold_pc: {silent_threshold_pc}')
	silent_th = int(silent_threshold_pc)/100
	print(f'\tsilent_th: {silent_th}')
	sound_s = 1
	print(f'\tsound_s: {sound_s}')
	silent_s = 999999
	print(f'\tsilent_s: {silent_s}')
	jumpcut_list = ['*_short_.wmv','*_short_.mp4','*_long__split*.mp4','*_short_.avi','*_short_.mkv','*_short_.mov']
	for data_type in jumpcut_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			no_of_file = len(nameList_F_withExt(current_dir,data_type))
			print(f'\tinFile: {inFile.upper()}, total of files in found inFile: {no_of_file}')
			f_name,f_ext = os.path.splitext(inFile)
			outFile = f_name+jumpcut_suffix +'.mp4'
			if os.path.exists(outFile):
				print(f'\toutFile: {outFile.upper()} is jumpcutted and existed')
			elif not os.path.exists(outFile):
				if jumpcut_suffix in inFile:
					print(f'\tinfile: {inFile.upper()} is already jumpcutted')
				if short_suffix in inFile or long_suffix in inFile and not os.path.exists(outFile) and not jumpcut_suffix in inFile:
					print(f'\tStart running JumpCutterUltra_PyoutFile to create outfile: {outFile}')
					JumpCutterUltra_Py(inFile,silent_th,sound_s,silent_s,margin,outFile)
	print('\tJumpcutting time: %s' % (dt.now() - stime_jc))
	#############################################
	#merge
	print(50*'-')
	print(' Merge setup:')
	if len(nameList_F_withExt(current_dir,'*_2merge_.txt'))==0:
		print(f'\tNo _2merge_ text file found, so nothing to merge')
	else:
		for inFile in nameList_F_withExt(current_dir,'*_2merge_.txt'):
			f_name,f_ext = os.path.splitext(inFile)
			f_name = f_name.replace('_2merge_','')
			outFile = f_name+'_jumpcut_merge_'+'.mp4'
			if os.path.exists(outFile):
				print(f'{outFile} is already existed')
			else:
				print(f'\tMerging inFile {inFile}')
				ffmpeg_merge_py(inFile,outFile)
				
	print(50*'-')
	print('Total Processing time: %s' % (dt.now() - stime))
if __name__ == "__main__":
	main()
