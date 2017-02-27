from ftplib import FTP

class FTPManager:
    
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password


    def connect(self, directory):
        ftp = FTP()
        ftp.connect(self.host, self.port)
        ftp.login(user = self.user, passwd = self.password)
        ftp.cwd(directory)
        return ftp


    def download(self, directory, filename):
        ftp = self.connect(directory)
        ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
        ftp.quit()


    def upload(self, directory, filename):
        ftp = self.connect(directory)
        ftp.storlines("STOR " + filename, open(filename, 'rb'))
        ftp.quit()
