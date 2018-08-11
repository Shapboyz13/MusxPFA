from pytube import YouTube
from flask import jsonify
import sys, subprocess, os

def ret_streams(url):
    if 'id' in url:
        yt = YouTube(url['url'])
        parent_dir = r"/home/shanky/Documents/Personal/MusxPFA/MusxPFA/static/music"
        stream = yt.streams.get_by_itag(int(url['id']))
        newFilename = "".join(stream.default_filename.split(".")[0:-1]) + '.mp3'
        # print ("\n\n", "data:",newFilename, "\n\n", file=sys.stdout)
        down = stream.download(parent_dir)
        if stream.default_filename.split(".")[-1]=="webm":
            subprocess.call([
                'ffmpeg',
                '-i',
                os.path.join(parent_dir, stream.default_filename),
                os.path.join(parent_dir, newFilename)])

            try:
                os.remove(os.path.join(parent_dir,stream.default_filename))
            except OSError:
                pass
        return True

    else:
        retdata = []
        yt = YouTube(url['url'])
        streams = yt.streams.filter().all()
        for stream in streams:
            data = str(stream).strip('<,>').split(' ')
            data = json_it(data);
            retdata.append({
                'name'          : stream.default_filename,
                'filesize'      : stream.filesize,
                'id'            : data['itag'],
                'type'          : data['mime_type'],
                'res'           : data['res'] if 'res' in data else "N/A",
                'fps'           : data['fps'] if 'fps' in data else "N/A",
                'abr'           : data['abr'] if 'abr' in data else "N/A",
            })
        return str(retdata)


def download(data):
    ret = ret_streams(data)
    if ret:
        return True
    else:
        return False


def json_it(data):
    retData = {}
    for x in data[1:]:
        retData[x.split("=")[0]] = x.split("=")[1].strip('"')
    return retData
