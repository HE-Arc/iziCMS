from FTPManager import FTPManager
from credentials import PWD

host = 'nexgate.ch'
user = 'j4kim'
port = 21
password = PWD
directory = 'exemple'
filename = 'index.html'

# creation du ftp manager
ftp = FTPManager(host,port,user,password)

# download
ftp.download(directory,filename)

# upload
ftp.upload(directory,filename)
