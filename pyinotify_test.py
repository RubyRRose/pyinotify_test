# !/usr/bin/env python
# -*- coding:UTF-8 -*-
import subprocess
import sys
import pyinotify

pos = 0 # 指针行位置(读取第几行)
file = "nohup.out"  # 脚本监控的日志文件 
error = "1000"  # 需要从日志中捕捉的字符串
finish = "end all job @..."  # 代表脚本整体执行结束的标志字符串 
source = "3.py"  # 需要杀死的脚本文件
callone = "ps -ef|grep -v grep|grep " + source + "|awk '{print $2}'|xargs kill -9"  # 杀死脚本文件的shell语句


def printlog():
    global pos
    try:
        fd = open(file)
        if pos != 0:
            fd.seek(pos, 0)
        while True:
            line = fd.readline()
            if line.strip():
                if error in line.strip():
                    subprocess.call(callone, shell=True)
                    fd.close()
                    sys.exit()
                if finish in line.strip():
                    fd.close()
                    sys.exit()
                pos = pos + len(line)
            if not line.strip():
                break
        fd.close()
    except Exception as e:
        print(str(e))
    finally:
        fd.close()


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        try:
            printlog()
        except Exception as e:
            print(str(e))


def main():
    printlog()
    wm = pyinotify.WatchManager()
    wm.add_watch(file, pyinotify.ALL_EVENTS, rec=True)
    eh = MyEventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


if __name__ == "__main__":
    main()

