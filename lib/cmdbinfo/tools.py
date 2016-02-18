#coding=utf-8
import cmdbinfo  as cmdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys,os

# sys.path.append('/data/ansiblework/')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))

# sys.path.append('/data/ansiblework/config/')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../config')))



from game import GAME_NAME
from games import HouTais


def donums(nums,skiphefu=False):
    '''是否跳过合服区,返回一个set,'''
    new=set()
    if skiphefu:
        for num in nums:
            ins=cmdb.cmdbinfo(num)
            # print num,str(num)==str(ins.hefu_baoliu())
            if str(num)==str(ins.hefu_baoliu()): new.add(num)   # 跳过合服区
    else:
        for num in nums:
            ins=cmdb.cmdbinfo(num)
            if ins.hefu_baoliu(): new.add(str(ins.hefu_baoliu()))  #不跳过合服区(将合服主区加入)
    return new


def grantdb(ip,port,user,passwd):
    '''授权函数: sqls在game.py中定义'''
    DB_CONNECT_STRING = r'mysql+mysqldb://%s:%s@%s:%s/?charset=utf8' % (user,passwd,ip,port)
    engine = create_engine(DB_CONNECT_STRING, echo=False)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    sqls=HouTais[GAME_NAME]['sqls']
    for sql in sqls:
        session.execute(sql).fetchall()
    session.commit()

def conv(adict):
    # ''' 传入一个字典重新构造一个字典(用于ansible)

    # {'group1': {'groupvars': {'gvar1': 'gvar2'},
    #             'hosts': {'host1': {'var1': 'var1', 'var2': 'var2'},
    #                       'host2': {'var3': 'var3', 'var4': 'var4'}}},
    #  'group2': {'hosts': {'host3': {'var5': 'var5', 'var6': 'var2'},
    #                       'host4': {'var7': 'var3', 'var8': 'var4'}}}}

    # '''

    # raw={}
    # raw['_meta']={}
    # raw['_meta']['hostvars']={}
    # hostslist={}
    # for gp,hlist in adict.items():
    #     raw[gp]=hlist.keys()
    #     raw['_meta']['hostvars'].update(hlist)
    # return raw



    raw={}
    raw['_meta']={}
    raw['_meta']['hostvars']={}
    for gname,ginfo in adict.items():
        raw[gname]={}
        raw[gname]['hosts']=ginfo['hosts'].keys()
        if 'groupvars' in ginfo:
            raw[gname]['vars']={}
            raw[gname]['vars'].update(ginfo['groupvars'])
        raw['_meta']['hostvars'].update(ginfo['hosts'])
    return raw

'''
adict={'group1': {'groupvars': {'gvar1': 'gvar2'},
                'hosts': {'host1': {'var1': 'var1', 'var2': 'var2'},
                          'host2': {'var3': 'var3', 'var4': 'var4'}}},
     'group2': {'hosts': {'host3': {'var5': 'var5', 'var6': 'var2'},
                          'host4': {'var7': 'var3', 'var8': 'var4'}}}}
pprint.pprint(conv(adict))
'''