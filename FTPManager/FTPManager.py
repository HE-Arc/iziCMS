from ftplib import FTP
import io

def connect(host, port, user, password, directory):
    ftp = FTP()
    ftp.connect(host, int(port))
    ftp.login(user=user, passwd=password)
    ftp.cwd(directory)
    return ftp

def download(host, port, user, password, directory, filename):
    try:
        ftp = connect(host, port, user, password, directory)
        r = io.BytesIO()
        if filename.startswith('/'):
            filename = filename[1:]
        ftp.retrbinary('RETR ' + filename, r.write)
        ftp.quit()
        return r.getvalue()
    except:
        return None

def upload(host, port, user, password, directory, filename, text):
    with connect(host, port, user, password, directory) as ftp:
        f = io.BytesIO(text.encode("utf-8"))
        if filename.startswith('/'):
            filename = filename[1:]
        ftp.storlines("STOR " + filename, f)


def test(host, port, user, password, directory = "/"):
    try:
        ftp = connect(host, port, user, password, directory)
        ftp.voidcmd("NOOP") # do nothing but raise an error in case of failure
        ftp.quit()
        return True
    except:
        return False
