# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:51:27 2020


@author: python MATLAB & GIS
"""
import datetime
import subprocess
import os
#import sys
import time
from moviepy.editor import VideoFileClip
current_dir = os.getcwd()
print(current_dir)

#%%
def main():
###########################################
#overal setup

	margin = input('Margin: ')
	silent_threshold_pc = input('silent_threshold percent: ') 
	jumpcut_suffix = 'jcmg'+margin+'_'+silent_threshold_pc+'pc'
#rename
			
	duration_sec = 1500
#	duration_sec = 30
	short_suffix = '_short_'
	long_suffix = '_long_'
	
	datatype_list = ['*.mp4','*.wmv','*.mov','*.avi']	
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			rename_based_on_length(inFile, duration_sec,short_suffix,long_suffix)
#######################
#Convert to mp4
	wmv2mp4_yn = input('Do u want to convert all *.wmv to mp4 files? (Y/N)')
	mp4_convert_yn = input('Do u want to process converted mp4:(Y/N)')
	if wmv2mp4_yn.upper() == 'Y':
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,'*.wmv')):
			f_name,f_ext = os.path.splitext(inFile)
			if mp4_convert_yn.upper() == 'Y':
				outFile = f_name +'.mp4'
				ffmpeg_wmv2mp4(inFile,outFile)
			else:
				outFile = f_name +'_convert_'+'.mp4'
				ffmpeg_wmv2mp4(inFile,outFile)
		
#############################################
#split
	for data_type in datatype_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):
			if '_jumpcut_merge_' in inFile:
				print(f'This is merged file: {inFile}, do not split it')
			elif '_convert_' in inFile:
				print(f'This is converted file: {inFile}, do not split it')
			else:
				split_new(inFile,duration_sec,jumpcut_suffix,short_suffix,long_suffix)
			

#############################################
#jumpcut
	silent_th = int(silent_threshold_pc)/100
	sound_s = 1
	silent_s = 999999
	jumpcut_list = ['*_short_.wmv','*_short_.mp4','*_long__split*.mp4']
	for data_type in jumpcut_list:
		for idx,inFile in enumerate(nameList_F_withExt(current_dir,data_type)):	
			f_name,f_ext = os.path.splitext(inFile)
			outFile = f_name+jumpcut_suffix +'.mp4'
			if jumpcut_suffix in inFile:	
				print(f'{jumpcut_suffix.upper()} is in {inFile.upper()} so \n\t so it already jumpcutted')
			elif os.path.exists(outFile): 
				print(f'{outFile.upper()} is already existed,\n\t which is jumpcuted from {inFile.upper()}')
			elif short_suffix in inFile or long_suffix in inFile: 
				print(inFile)
				print(outFile)
				JumpCutterUltra_Py(inFile,silent_th,sound_s,silent_s,margin,outFile)
#############################################
#merge
	for inFile in nameList_F_withExt(current_dir,'*_2merge_.txt'):
		f_name,f_ext = os.path.splitext(inFile)
		f_name = f_name.replace('_2merge_','')
		outFile = f_name+'_jumpcut_merge_'+'.mp4'
		if os.path.exists(outFile): 
			print(f'{outFile} is already existed')
		else: 
			ffmpeg_merge_py(inFile,outFile)
#%%
##############################################################################
def ffmpeg_wmv2mp4(inFile,outFile):
	ffmpegFile = "D:/Downloads/youtube-dl/ffmpeg.exe"
	print('Running ffmpeg_wmv2mp4:{ffmpegFile} ' )
	print(f'\t Input :{inFile}; Output :{outFile}')
	subprocess.call([ffmpegFile,'-i',inFile,outFile])
	print(f'\t\t\t\done with {outFile}')
#for %%f in (*.wmv) DO ffmpeg -i %%f %%f.mp4
##############################################################################
def ffmpeg_merge_py(inFile,outFile='jumpcut_merge_'):
	ffmpegFile = "D:/Downloads/youtube-dl/ffmpeg.exe"
	print('Running ffmpeg_merge_py:{ffmpegFile} ' )
	print(f'\t Input :{inFile}; Output :{outFile}')
	subprocess.call([ffmpegFile,'-f', 'concat','-i',inFile,'-c','copy',outFile])
	print(f'\t\t\t\done with {outFile}')
##############################################################################
def JumpCutterUltra_Py(inFile,silent_th,sound_s,silent_s,margin,outFile):
	JumpCutterUltraFile = "C:/Davince Resolve 16/JumpCutterUltra/JumpCutterUltra.exe"
	print(f'Running JumpCutterUltra_Py {JumpCutterUltraFile}')
	print(f'\t Input :{inFile}; Output :{outFile}')
	subprocess.call([JumpCutterUltraFile,'--input_file',inFile,'--silent_threshold',str(silent_th),'--sounded_speed',str(sound_s),'--silent_speed',str(silent_s),'--frame_margin',margin,'--output_file',outFile])
	print(f'\t\t\t\done with {outFile}')
###############

def ffmpeg_split(inFile,outFile,start_point,duration_sec):
	ffmpegFile = "D:/Downloads/youtube-dl/ffmpeg.exe"
	print('Running ffmpeg_split:{ffmpegFile} ' )
	print(f'\t Input :{inFile}; Output :{outFile}')
	subprocess.call([ffmpegFile,'-i',inFile,'-ss',str(start_point),'-t',str(duration_sec),outFile])
	print(f't\t\t\done with {outFile}')
# ffmpeg -i t.mp4 -ss 00:00:00 -t 2440 -c:v h264_nvenc t_split1.mp4

##### split based on duration function #########################
###############################################################################

def split_new(inFile,duration_sec,jumpcut_suffix,short_suffix,long_suffix):

	print('\n\n\n'+100*'#')
	start_point = 0
	overlap_duration = 2
	clipped_length = duration_sec + overlap_duration
	
	in_name,in_ext = os.path.splitext(inFile)
	inFile_length = clip_duration(inFile)
	if inFile_length <= duration_sec+duration_sec/2 and short_suffix in inFile:
		print(f'This video is short {inFile}, no clipping required, length: {inFile_length} sec or {get_strtime(inFile_length)}')
#		pass
	if inFile_length > duration_sec+duration_sec/2 and 'split' not in inFile and long_suffix in inFile:
		#create a text file to merge laters
		out_ffmpeg_merge_txtf = open(in_name+'_2merge_.txt','w')
		no_clipped_segments = int(inFile_length/duration_sec)+1
		#%
		for i in range(no_clipped_segments):
			msg = 'file '+ "'"+in_name+ '_split' + str(i+1) + jumpcut_suffix +'.mp4'+"'"
			print(msg)
			out_ffmpeg_merge_txtf.write(msg+'\n')
		out_ffmpeg_merge_txtf.close()
#		for each segment	
		for i in range(no_clipped_segments):
			outFile = in_name+ '_split' + str(i+1) + '.mp4' 			#segment name
			if os.path.exists(outFile): 
				print(f'\t\toutFile already exists: {outFile}')
#				pass
			if not os.path.exists(outFile):
				print(f'\tCreating cliped file No{i+1}: {outFile}')
				if i == 0:		 
					start_point = i*duration_sec
					clipped_length_first = clipped_length-overlap_duration/2
					ffmpeg_split(inFile,outFile,start_point,clipped_length_first)
					print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length_first}')
				elif i == max(range(no_clipped_segments)):
					start_point = i*duration_sec-overlap_duration/2
					clipped_length_last = inFile_length%duration_sec+overlap_duration/2
					ffmpeg_split(inFile,outFile,start_point,clipped_length_last)
					print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length_last}')
				else:			
					start_point = i*duration_sec-overlap_duration/2
					ffmpeg_split(inFile,outFile,start_point,clipped_length)
					print(f'\t\t\tinFile:{inFile}\n\t\t\toutFile:{outFile}\n\t\t\tstart_point:{start_point}\n\t\t\tclipped_length:{clipped_length}')
	print(100*'#'+'\n')
### rename ##########################################################
def rename_based_on_length(inFile, duration_sec,short_suffix,long_suffix):
	print(80*'-')
	print('Clip_duration: {duration_sec} ~ {duration_sec/60} mins')
	print(f'InFile: {inFile}')
	f_name,f_ext = os.path.splitext(inFile)
	temp_name =f_name.replace('-','_')
	temp_name =temp_name.replace('-','_')
	temp_name =temp_name.replace('-','_')
	temp_name =temp_name.replace(' ','')
	temp_name =temp_name.replace(' ','')
	inFile_length = clip_duration(inFile)
	if (short_suffix in temp_name):
		print(f'\t is already RENAMED and INCLUDED {short_suffix}')
	elif (long_suffix in temp_name):
		print(f'\t already RENAMED and INCLUDED {long_suffix}')
	elif (inFile_length <= duration_sec+duration_sec/2) and (short_suffix not in temp_name):
		new_name = temp_name+short_suffix+f_ext
		print(inFile,inFile_length,' ==> ',new_name)
		os.rename(inFile, new_name)
	elif (inFile_length > duration_sec+duration_sec/2) and (long_suffix not in temp_name):
		new_name = temp_name+long_suffix+f_ext
		print(inFile,inFile_length,' ==> ',new_name)
		os.rename(inFile, new_name)
	else: print('Something wrong: check rename_based_on_length')
	print(80*'-'+'\n')

#############################################################################
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
############################################################################
	
def clip_duration(invideoF):
	from moviepy.editor import VideoFileClip
	clip = VideoFileClip(invideoF)
	clip_duration = clip.duration
	clip.close()
	return clip_duration
#print(clip_duration('0_20120829_matlab_ValSchmidt_split1_cut1.mp4','hms'))
#print(clip_duration('0_20120829_matlab_ValSchmidt_split1_cut1.mp4','sec'))
###########################################################################
#make a dictionary of file name and length
	#required nameList_F_withExt , clip_duration
def name_length_dic_define(in_dir,data_type):
	name_length_dic = {}
	for inFile in nameList_F_withExt(in_dir,data_type):
		inFile_length = clip_duration(inFile)
		name_length_dic[inFile]=inFile_length
	return name_length_dic
#make a list of name_length_list
def name_length_list_define(in_dir,data_type):
	name_length_list = []
	for inFile in nameList_F_withExt(in_dir,data_type):
		inFile_length = clip_duration(inFile)
		name_length_list.append([inFile,inFile_length])
	return name_length_list
#%% testing
#in_dir = os.getcwd()
#in_dir
#data_type = '*.mp4'
#file1 = nameList_F_withExt(in_dir,data_type)[0]
#file1
#inFile_length = clip_duration(file1)
#inFile_length
#n_l_dic = name_length_dic_define(in_dir,data_type)
#n_l_dic.keys()
#
#n_l_lst = name_length_list_define(in_dir,data_type)
#n_l_lst
#n_l_lst[0][1]
#%%
if __name__ == "__main__": 
	main()
