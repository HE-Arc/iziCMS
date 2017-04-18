from ftplib import FTP
import io

def connect(host, port, user, password, directory):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(user = user, passwd = password)
    ftp.cwd(directory)
    return ftp

def download(host, port, user, password, directory, filename):
    ftp = connect(host, port, user, password, directory)
    r = io.BytesIO()
    text = ftp.retrbinary('RETR ' + filename, r.write)
    ftp.quit()
    return r.getvalue()

def upload(host, port, user, password, directory, filename, text):
    ftp = connect(host, port, user, password, directory)
    f = io.BytesIO(text.encode("utf-8"))
    ftp.storlines("STOR " + filename, f)
    ftp.quit()


def test(host, port, user, password):
    try:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(user = user, passwd = password)
        ftp.voidcmd("NOOP") # do nothing but raise an error in case of failure
        ftp.quit()
        return True
    except:
        return False
    