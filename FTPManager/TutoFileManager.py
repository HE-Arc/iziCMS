from FTPManager import FTPManager
host = 'nexgate.ch'
user = 'j4kim'
port = 21
password = 'iwc37QNA'
directory = 'exemple'
filename = 'index.html'

# creation du ftp manager
ftp = FTPManager(host,port,user,password)

# download
ftp.download(directory,filename)

# upload
ftp.upload(directory,filename)
