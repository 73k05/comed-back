# Write in Log file
def writeLog( str ):
	f=open("output.txt", "a+")
	f.write(str)
	f.close()
	return