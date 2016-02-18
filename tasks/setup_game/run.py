#coding=utf-8

import os,sys,pprint,json
from ansible.color import stringc

#这里定义了将要更新的区
from zone import *

curdir=os.path.dirname(os.path.abspath(__file__))

#将项目主目录加入python系统搜索路径, 使可以查找到game.py、config目录
#这里指向operansible目录
sys.path.append(os.path.abspath(os.path.join(curdir,'../..')))
from game import GAME_NAME
from config.games import LOGFILE

#将库目录lib加入python系统搜索路径
sys.path.append(os.path.abspath(os.path.join(curdir,'../../lib')))
from public import _tee,nowtime
import cmdbinfo as cmdb
from ansibleapi.do import job
from cmdbinfo import tools

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'project'))
main=__import__(GAME_NAME)

# ansible需要的site.py
siteyml=os.path.join(os.path.dirname(os.path.abspath(__file__)),'site.yml')

#定义脚本执行的日志
rsfile=os.getcwd()+'/rs.txt'
open(rsfile,'w').close()
logging_tmp=_tee(rsfile,'a+')
logging=file(LOGFILE,'a+')
logging_tmp._write('[ '  + '='*15 + nowtime() + '='*15 + ' ]')


start=start.strip()
end=end.strip()
mobannum=mobannum.strip()
nums=set(tmp_nums.split())

if not mobannum: sys.exit('zone.conf中未指定模版区号')

if (bool(nums)==True and bool(start)==False and bool(end)==False) or (bool(nums)==False and start and end):
    print '正在以%s服为模版部署后端: %s - %s ' % (stringc(mobannum,'green'),stringc(start,'green'),stringc(end,'green')) \
    if start and end else \
    '正在以%s服为模版部署后端: %s' % (stringc(mobannum,'green'), stringc(' '.join(nums),'green'))

    logging_tmp._write(('正在以%s服为模版部署后端: %s - %s ' % (mobannum,start,end)) \
        if start and end else \
        ('正在以%s服为模版部署后端: %s' % (mobannum,' '.join(nums))))

    rep=raw_input('输入y继续: ')
    if rep.lower() != 'y': sys.exit('已退出')

    mo=cmdb.cmdbinfo(mobannum)
    try:
        mo_javaip=mo.backendinfo()[0]
        real_num=mo.hefu_baoliu()
    except:
        sys.exit('错误,可能是该区已经删除,请重新指定打模版区')

    skiphefu=False
    if not nums:
        nums=[str(i) for i in range(int(start),int(end)+1)]
        skiphefu=True

    adict={'do_moban':{'hosts':{}},'setup_game':{'hosts':{}}}
    adict['do_moban']['hosts']={'moban_'+str(mobannum):{'num':real_num, 'ansible_ssh_host':mo_javaip},}
    nums=tools.donums(nums,skiphefu=skiphefu)
    adict=main.handle(nums,adict)

else:
    print '区信息配置错误,请修正conf.py'

logging_tmp._write(pprint.pformat(adict))
logging_tmp.close()
raw=tools.conv(adict)

ret=job(siteyml,json.dumps(raw),rsfile)
logging_tmp=_tee(rsfile,'a+')
logging_tmp._write(ret)
logging_tmp.close()
rs_f=open(rsfile)
logging.write(rs_f.read())
logging_tmp.close()
rs_f.close()
