# Write in Log file
def write_log(logmessage):
    print(logmessage)
    if isinstance(logmessage, str):
        f = open("output.txt", "a+")
        f.write(logmessage)
        f.write("\r\n")
        f.close()
    return


# Write in Log file
def write_server_log(log_message):
    print(log_message)
    if isinstance(log_message, str):
        f = open("server.log", "a+")
        f.write(log_message)
        f.write("\r\n")
        f.close()
    return
