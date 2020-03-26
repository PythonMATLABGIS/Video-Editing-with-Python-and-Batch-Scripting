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
	#define clipping information
	start_point = 0
	duration_sec = 1500
	overlap_duration = 4
	clipped_length = duration_sec + overlap_duration

	#########################################################################################################
	#looping through all files and clip

	print('\n\n\n'+100*'#')

	#jumpcut_suffix = input('Input jumcut suffix (eg. _margin1- this have to be the same with output for jumpcut): ') 
	#---------------------------------------------------------------------------------------------------
	#-------change jumpcut_suffix before running %%f_jcmg1.mp4
	jumpcut_suffix = '.mp4_jcmg1'
	# this will be use for merging later

	for idx,inFile in enumerate(nameList_F_withExt(current_dir,'*.wmv')):
		print(100*'-')
		#print(f'Input File Id No: {idx}, name: {inFile}')
	#	inFile = '2_20120830_matlab3_ValSchmidt.mp4'
		in_name,in_ext = os.path.splitext(inFile)
		out_ffmpeg_merge_txtf = open(in_name+'.txt','w')
		inFile_length = clip_duration(inFile)
		if inFile_length <= duration_sec+600:
			pass
			print(f'This video is short, no clipping required, length: {inFile_length} sec or {get_strtime(inFile_length)}')
		else:
			clip_number = int(inFile_length/duration_sec)+1
			#%%
			for i in range(clip_number):
				outFile = in_name+ '_split' + str(i+1) + '.mp4'
				msg = 'file '+ "'"+in_name+ '_split' + str(i+1) + jumpcut_suffix +'.mp4'+"'"
				out_ffmpeg_merge_txtf.write(msg+'\n')

				
			for i in range(clip_number):
				outFile = in_name+ '_split' + str(i+1) + '.mp4'
				msg = 'file '+ "'"+in_name+ '_split' + str(i) + jumpcut_suffix +'.mp4'+"'"
				print(f'\tClipping No{i}: {outFile}')
				if i == 0:		 
					start_point = i*duration_sec
					clipped_length_first = clipped_length-overlap_duration/2
					end_point = start_point + clipped_length_first
					if os.path.exists(outFile):
						pass
						print(f'\t\toutFile already exists: {outFile}')
					else: 
						ffmpeg_split(inFile,outFile,start_point,clipped_length_first)
						print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length_first}')
				elif i == max(range(clip_number)):
					start_point = i*duration_sec-overlap_duration/2
					clipped_length_last = inFile_length%duration_sec+overlap_duration/2
					end_point = start_point + clipped_length_last
					if os.path.exists(outFile):
						pass
						print(f'\t\toutFile already exists: {outFile}')
					else: 
						ffmpeg_split(inFile,outFile,start_point,clipped_length_last)
						print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length_last}')
				else:			
					start_point = i*duration_sec-overlap_duration/2
					end_point = start_point + clipped_length
					if os.path.exists(outFile):
						pass
						print(f'\t\toutFile already exists: {outFile}')
					else: 
						ffmpeg_split(inFile,outFile,start_point,clipped_length)
						print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length}')
					
	#plotting details only
			# print("\n################-plotting details only - ##########################")
			# for i in range(clip_number):
				# outFile = in_name+ '_split' + str(i) + '.mp4'
				# print(f'\tClip No{i}: {outFile}')
				# if i == 0:		 
					# start_point = i*duration_sec
					# print('\t\t starting point:',start_point)
					# clipped_length_first = clipped_length-overlap_duration/2
					# print(f'\t\t clipped_length_first: {clipped_length_first}')
					# end_point = start_point + clipped_length_first
					# print('\t\t ending point:',end_point)
			# #		ffmpeg_split(inFile,outFile,start_point,clipped_length_first)
				# if i == max(range(clip_number)):
					# start_point = i*duration_sec-overlap_duration/2
					# print('\t\t starting point:',start_point)
					# clipped_length_last = inFile_length%duration_sec+overlap_duration/2
					# print(f'\t\t clipped_length_last: {clipped_length_last}')
					# end_point = start_point + clipped_length_last
					# print('\t\t ending point:',end_point)
			# #		ffmpeg_split(inFile,outFile,start_point,clipped_length_last)
				# else:			
					# start_point = i*duration_sec-overlap_duration/2
					# print('\t\t starting point:',start_point)
					# print(f'\t\t clipped_length: {clipped_length}')
					# end_point = start_point + clipped_length
					# print('\t\t ending point:',end_point)
			# #		ffmpeg_split(inFile,outFile,start_point,clipped_length)
			#	

	print(100*'#'+'\n')
	out_ffmpeg_merge_txtf.close()


#%
def clip_duration(invideoF):
	from moviepy.editor import VideoFileClip
	clip = VideoFileClip(invideoF)
	return clip.duration


		
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
	import time
	return time.strftime('%H:%M:%S', time.gmtime(time_sec))
#get_strtime(5025)


def ffmpeg_split(inFile,outFile,start_point,duration_sec):
	ffmpegFile = "D:/Downloads/youtube-dl/ffmpeg.exe"
	subprocess.call([ffmpegFile,'-i',inFile,'-ss',str(start_point),'-t',str(duration_sec),outFile])
# ffmpeg -i t.mp4 -ss 00:00:00 -t 2440 -c:v h264_nvenc t_split1.mp4

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
