from telnetlib import Telnet
from pathlib import Path
import re
import requests


def main():
    # Establishing Telnet connection with the camera
    tn = Telnet('192.168.42.1', 0, 1000)
    tn.read_until(b"login: ")
    tn.write(b"root\n")
    tn.read_until(b"#")
    # Getting video files list
    tn.write(b"cd /var/www/DCIM/100MEDIA\n")
    tn.read_until(b"#")
    tn.write(b"ls\n")
    files_string = tn.read_until(b"#").decode("ascii")
    files = [m for m in re.findall('VID[0-9]*.MP4', files_string)]
    print("Found " + str(len(files)) + " videos. Download the last (L) one or all (A)?")
    download_option = input()
    if download_option.lower() == "l":
        download(files[-1])
    elif download_option.lower() == 'a':
        for file in files:
            download(file)


def download(filename):
    print("Downloading " + filename + "...")
    url = "http://192.168.42.1/DCIM/100MEDIA/" + filename
    r = requests.get(url)
    path = str(Path.home()) + "/ghost-videos/"
    Path(path).mkdir(parents=True, exist_ok=True)
    f = open(path + filename, "wb+")
    f.write(r.content)
    f.close()
    print('Finished!')


main()
