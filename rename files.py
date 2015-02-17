import os

dirpath = "C:\\Users\\Alexandru\\Desktop\\Git\\Indycoding\\Memo-Boo\\app\\src\\main\\assets\\bloody"
for filename in os.listdir(dirpath):
	print (filename)
	# if filename.startswith("cheese_"):
	newname = dirpath + '\\bl_' + filename
	os.rename(dirpath + '\\' + filename, newname)