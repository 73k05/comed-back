# Write in Log file
def writeLog(logmessage):
    print(logmessage)
    if isinstance(logmessage, str):
        f = open("output.txt", "a+")
        f.write(logmessage)
        f.write("\r\n")
        f.close()
    return
