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
###########################################
def main():
	stime = dt.now()
	merge_prefix = input('merge prefix:')
	jumpcut_suffix = input('Suffix for merge file: (1_5pc):')
	#Generate text for merge
	out_ffmpeg_merge_txtf = open('_2merge_.txt','w')	
	for idx,inFile in enumerate(nameList_F_withExt(current_dir,'*.mp4')):
		in_name,in_ext = os.path.splitext(inFile)
		msg = 'file ' + "'" + inFile + "'"
		out_ffmpeg_merge_txtf.write(msg+'\n')
		
	out_ffmpeg_merge_txtf.close()
	
	#-----------------------------------------------------------------------
	#merge
	print(50*'-')
	print(' Merge setup:')
	merge_suffix = '_jumpcut_merge_'+jumpcut_suffix
	if len(nameList_F_withExt(current_dir,'*_2merge_.txt'))==0:
		print(f'\tNo _2merge_ text file found, so nothing to merge')
	else:
		for inFile in nameList_F_withExt(current_dir,'*_2merge_.txt'):
			f_name,f_ext = os.path.splitext(inFile)
			f_name = f_name.replace('_2merge_','')
			outFile = merge_prefix+f_name+merge_suffix+'.mp4'
			if os.path.exists(outFile):
				print(f'{outFile} is already existed')
			else:
				print(f'\tMerging inFile {inFile}')
				ffmpeg_merge_py(inFile,outFile)
				
	print(50*'-')
	print('Total Processing time: %s' % (dt.now() - stime))
if __name__ == "__main__":
	main()