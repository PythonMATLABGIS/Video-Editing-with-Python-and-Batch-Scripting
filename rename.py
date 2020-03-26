import os
current_dir = os.getcwd()
print(current_dir)

#list all file with extentions
def nameList_F_withExt(InputFolder,filterString="*"):
	import glob	
	os.chdir(InputFolder) #change working folder
	return glob.glob(filterString)

#rename
for idx,f in enumerate(nameList_F_withExt(current_dir,'*.wmv')):
	print(f)
	f_name,f_ext = os.path.splitext(f)
	temp_name = f_name.replace('Định vị và đo sâu biển','Dinh vi va do sau bien')
	temp_name =temp_name.replace('-','_')
	temp_name =temp_name.replace(',','')
	temp_name =temp_name.replace(' ','')
	new_name = str(idx+1)+'_'+temp_name+f_ext
	os.rename(f, new_name)
	print(new_name)


