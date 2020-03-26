import os
import glob
current_dir = os.getcwd()  #the folder containing the python script


#list all file with extensions and sorted by datetime
def nameList_F_withExt_byTime(InputFolder,filterString="*"):
	os.chdir(InputFolder) #change working folder
	nameList = glob.glob(filterString)
	nameList.sort(key=os.path.getctime)
	return nameList

#sort by time and rename
for idx,f in enumerate(nameList_F_withExt_byTime(current_dir,'*.wmv')):
	# print(f)
	f_name,f_ext = os.path.splitext(f)
	temp_name = f_name.replace('Định vị và đo sâu biển','Dinh vi va do sau bien')
	temp_name =temp_name.replace('-','_')
	temp_name =temp_name.replace('-','_')
	temp_name =temp_name.replace(' ','')
	temp_name =temp_name.replace(' ','')
	new_name = temp_name+f_ext
	os.rename(f, new_name)
	print(new_name)


