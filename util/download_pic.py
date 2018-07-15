#!/usr/bin/env python3
# coding: utf-8
# UTF-8です

import os, pickle, random, requests, time

ID_PICKLE_FILE = "valid_ids.pickle"
PIC_OUTPUT_DIR = "../download"
PIC_EXCLUDE_DIRS = "../annotation", "../download"

execdir = os.path.dirname(os.path.abspath(__file__))

# load ids
danbooru_ids = None
with open(os.path.join(execdir, ID_PICKLE_FILE), 'rb') as f:
    danbooru_ids = set(pickle.load(f))
    
#exclude downloaded ids
for dir in PIC_EXCLUDE_DIRS:
    for root, dirs, files in os.walk(os.path.join(execdir, dir)):
        for fn in files:
            id, ext = os.path.splitext(fn)
            try:
                danbooru_ids.remove(id)
            except KeyError:
                pass
        


def save_image(filepath, img):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as w:
        w.write(img)
    
def download_pic(url, timeout=10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        raise IOError("HTTP status:", response.status_code)
        
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        raise TypeError("Content-Type:", content_type)
        
    return response.content
    
def getfilepath(id, url, download_dir=os.path.join(execdir, PIC_OUTPUT_DIR)):
    _, ext = os.path.splitext(url)
    filename = "{}{}".format(id, ext)
    #if outpath==None:
    outpath = os.path.join(execdir, PIC_OUTPUT_DIR, filename)
    return outpath
    
def danbooruid_to_url(id):
    url = "https://danbooru.donmai.us/posts/{}.json".format(id)
    response = requests.get(url)
    jsondata = response.json()
    #print(jsondata)
    #リクエストのエラーと画像が存在しないエラーを分けた方がいい?
    if "file_url" not in jsondata:
        #raise IOError("Requesting JSON file failed. Please try again later.")
        # if request error, should retry later.
        # if request succeeded but no "file_url", just ignore
        return None
    file_url = jsondata["file_url"]
    # skip if not a image file
    _, ext = os.path.splitext(file_url)
    if ext not in (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".gif"):
        return None
    return file_url
    
    
def get_random_danbooru_id():
    id = random.sample(danbooru_ids, 1)[0]
    danbooru_ids.remove(id)
    return id
    # Giving an empty list raises IndexError.
    
def download_random_pic():
    id = get_random_danbooru_id()
    url = danbooruid_to_url(id)
    while url is None:
        id = get_random_danbooru_id()
        url = danbooruid_to_url(id)
    print("Downloading:", id)
    #ファイル名は{danbooruid}.{ext}形式にする。
    fpath=getfilepath(id, url)# getfilepathをid, url, basedirとして、Danbooru2017データセットと同じ構造を返すようにする?
    img = download_pic(url)
    save_image(fpath, img)
    
def download_random_pics(n):
    for i in range(n):
        download_random_pic()
        time.sleep(2)
    
    
if __name__ == '__main__':
    #for i in range(5):
    #    print(danbooruid_to_url(get_random_danbooru_id()))
    #レーティングもデータとして欲しい。エロ画像をダウンロードしたくない場合用に
    download_random_pics(100)
    