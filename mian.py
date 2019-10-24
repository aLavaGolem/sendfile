from watchdog.observers import Observer
from watchdog.events import *
import time
import shutil
import re
import os


#tomcat webapps根目录
webappsPath ="C:\\Users\\skyjian\\wtpwebapps\\"
#eclipse项目地址
eclipsePath="C:\\eclipse-workspace\\"
dict = {}
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
            if event.src_path.find("src")!=-1:
                print("-----------------------------------")
        else:
            print("file modified:{0}".format(event.src_path))
            #判断是src下
            if event.src_path.find("src") != -1:
                #获取文件后缀
                suffix=os.path.splitext(event.src_path)
                print(eclipsePath.replace("\\","\\\\").replace("-","\-").replace(":","\:")+"(\\w+)src")
                #正则查找生成path
                r=re.match(eclipsePath.replace("\\","\\\\")+"(.+)src",event.src_path)
                path=r.group(0)
                projectName=r.group(1)
                newPath=webappsPath+projectName+"WEB-INF\\classes";
                libPath=webappsPath+projectName+"WEB-INF\\lib";

                pn=projectName.replace("\\","")

                fpath=event.src_path.replace(path,newPath)
                dpath ="-d "+newPath+" ";
                print(fpath+"        最后的path")
                # 判断文件后缀
                if suffix[1]==".java":
                    # javac
                    libstr = ""
                    if pn in dict.keys():
                        libstr = dict[pn]
                    else:
                        dirlist = os.listdir(libPath)
                        for v in dirlist:
                            libstr += ";\"" + libPath + "\\" + v+"\""
                        dict[pn] = libstr
                    # print(fpath.replace(suffix[1],"\.class"))
                    if os.path.exists(fpath.replace(suffix[1],".class")):
                        print("删除成功")
                        os.remove(fpath.replace(suffix[1],".class"))
                    time.sleep(1)
                    print("休眠了1秒钟")
                    javacstr = "javac  -Xlint:unchecked -encoding utf-8  -classpath " + path + libstr + ";D:\\JAVA\\apache-tomcat-8.5.43\\lib\\servlet-api.jar  "+dpath+ event.src_path;
                    r=os.popen(javacstr);
                    print(r.read())

                else:
                    shutil.copyfile(event.src_path,fpath)
                    print("复制成功")


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,"C:\\eclipse-workspace",True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()