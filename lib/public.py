#coding=utf-8


import sys,time
class _tee(file):
    def write(self, text):
        sys.stdout.write(text)
        file.write(self, str(text)+'\n')

    def _write(self, text):
        file.write(self, str(text)+'\n')


def nowtime():
    return time.strftime(' %Y-%m-%d %H:%M:%S ',time.localtime(time.time()))

def nowtime_int():
    return time.time()

if __name__ == '__main__':
    with _tee('/tmp/test.txt','a+') as f:
        f.write('something .... ')
        f._write('something else ... ')
