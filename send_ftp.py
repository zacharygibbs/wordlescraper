import json, os
import ftplib
##https://www.geeksforgeeks.org/how-to-download-and-upload-files-in-ftp-server-using-python/
with open('secret_web.json', 'r') as f:
    sec = json.load(f)
# Connect FTP Server
ftp_server = ftplib.FTP(sec['host'], sec['username'], sec['password'])
# force UTF-8 encoding
ftp_server.encoding = "utf-8"
# Enter File Name with Extension
filename = "wordlestats_list.csv"
upload_path = 'public_html/data'
# Read file in binary mode
with open(filename, "rb") as file:
    # Command for Uploading the file "STOR filename"
    ftp_server.storbinary(f"STOR {os.path.join(upload_path,filename)}", file)
# Get list of files
ftp_server.dir(os.path.join(upload_path,filename))
# Close the Connection
ftp_server.quit()