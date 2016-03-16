# -* - coding: UTF-8 -* -
import urllib.request
import os
import threading
import json
import socket
import time

# #建立线程池，并启动线程直到结束
def parallel(infos):
    startTime = time.time()
    threads=[]
    counts = range(len(infos))
    for i in counts:
        t=MyThread(downloadImage,(infos[i],),downloadImage.__name__)
        threads.append(t)
    for i in counts:
        threads[i].start()
    for i in counts:
        threads[i].join()
    print('花费时间:%s'%(time.time()-startTime))

# #自定义线程类
class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        self.res=self.func(*self.args)

# # #建立线程池，并启动线程直到结束
# def parallel(infos):
#     counts = range(len(infos))
#     for i in counts:
#         downloadImage(infos[i])
#     print("OK")

#根绝imageUrl下载图片到本地
def downloadImage(info):
    imageUrl = info["url"]
    imagePName = info["pname"]
    imageCName = str(info["cname"])
    dir = "./"+imagePName+"/"
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
    except Exception as e:
        print("创建目录失败 %s"%dir)
        print(e)
        exit()
    imageType = imageUrl.split('.')[-1]
    path = dir+imageCName + "."+imageType
    if os.path.exists(path):
        print("文件已存在")
    else:
        print("文件不存在")
        try:
            data = urllib.request.urlopen(imageUrl).read()
        except:
            print("下载失败")
        try:
            f = open(path,"wb")
            f.write(data)
            f.close()
            print("保存成功"+path)
        except:
            print("保存失败")

#下载整个相册
def downloadAlbum(albumName,albumIndex):
    reqs =[]
    try:
        res = urllib.request.urlopen("http://acgstay.mavericks.lol:8888/index?index="+albumIndex+"&mode=3")
        resAlbum = json.loads(res.read().decode('utf-8'))
    except:
        print("获取专辑信息失败")
    for Album in resAlbum['info']:
        # print("文件名：" + Album['tags'] + " 文件ID：" + str(Album['id']) + " 下载地址：" + Album['url'])
        a = {}
        a['pname'] = albumName
        a['cname'] = Album['id']
        a['url'] = Album['url']
        reqs.append(a)
    parallel(reqs)

#获取专辑信息
def downloadIndex():
    try:
        res = urllib.request.urlopen("http://acgstay.mavericks.lol:8888/index?index=mainindex&mode=3")
        resAlbum = json.loads(res.read().decode('utf-8'))
        print(resAlbum)
    except:
        print("获取索引失败")
    for Album in resAlbum['indexes']:
        print("开始下载专辑" + Album['des'] +" 索引是：" + Album['index'])
        downloadAlbum(Album['des'],Album['index'])
    print("结束任务")

if __name__ == "__main__":

    timeout = 10
    socket.setdefaulttimeout(timeout)
    downloadIndex()
