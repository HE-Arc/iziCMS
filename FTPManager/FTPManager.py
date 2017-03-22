from ftplib import FTP
import io

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

    def downloadRead(self, directory, filename):
        ftp = self.connect(directory)
        r = Reader()
        ftp.retrbinary('RETR ' + filename, r)
        ftp.quit()
        return r.data

    def upload(self, directory, filename):
        ftp = self.connect(directory)
        ftp.storlines("STOR " + filename, open(filename, 'rb'))
        ftp.quit()

    def uploadTextInFile(self, directory, filename, text):
        ftp = self.connect(directory)
        f = io.BytesIO(text.encode("utf-8"))
        ftp.storlines("STOR " + filename, f)
        ftp.quit()

class Reader:
  def __init__(self):
    self.data = ""
  def __call__(self,s):
     self.data += s.decode("utf-8")
