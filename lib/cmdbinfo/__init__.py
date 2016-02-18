#coding=utf-8
import sys
sys.path.append('/data/work/')
from game import GAME_NAME,PLATFORM
from config.games import HouTais

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import time,traceback

CMDB=HouTais[(GAME_NAME+PLATFORM)]

cmdbip     =CMDB['CMDB_IP']
cmdbport   =CMDB['CMDB_PORT']
cmdbname   =CMDB['CMDB_NAME']
cmdbpasswd =CMDB['CMDB_PASSWD']
cmdbuser   =CMDB['CMDB_USER']

VMTABLE    =CMDB['VMTABLE']
ROLETABLE  =CMDB['ROLETABLE']
GAMETABLE  =CMDB['GAMETABLE']
PORTTABLE  =CMDB['PORTTABLE']
no_update_zone=CMDB['no_update_zone']


DB_CONNECT_STRING = r'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (cmdbuser,cmdbpasswd,cmdbip,cmdbport,cmdbname,)
# print DB_CONNECT_STRING
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()




def errinfo():
    time.sleep(0.2)
    aaa=sys.exc_info()
    traceback.print_exception(aaa[0],aaa[1],aaa[2])

class cmdbinfo(object):
    def __init__(self,num):
        self.num=num

    def __str__(self):
        return '<cmdbinfo instance %s : zone: %s>' % (id(self),self.num)

    def dbinfo(self):
        '''A tuple: (dbip, dbport)'''
        sql="select av_vmip,av_dbport from %s where sysid in (select ar_vmid   from    %s where ar_zoneid='%s' and ar_typeid=2);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def slaveinfo(self):
        '''A tuple: (slaveip,slaveport,slavepassword)'''
        sql="select av_vmip,av_dbport,av_dbpass from %s where av_masterid=(select ar_vmid from   %s where ar_zoneid='%s' and ar_typeid=2);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def to_dbinfo(self):
        '''A tuple: (to_dbip, to_dbport)'''
        sql="select av_vmip,av_dbport from %s where sysid in (select ar_tovmid from    %s where ar_zoneid='%s' and ar_typeid=2);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def to_slaveinfo(self):
        '''A tuple: (to_slaveip,to_slaveport,to_slavepassword)'''
        sql="select av_vmip,av_dbport,av_dbpass from %s where av_masterid=(select ar_tovmid from %s where ar_zoneid='%s' and ar_typeid=2);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def dbnameinfo(self):
        '''A tuple: (dbname, to_dbname)'''
        sql="select ab_dbname,ab_todbname from %s where ab_zoneid='%s';" % (GAMETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

##################################################################################
    def backendinfo(self):
        '''A tuple: (javaip, javaname)'''
        sql="select av_vmip,av_domainname from %s where sysid in (select ar_vmid from %s where ar_zoneid='%s' and ar_typeid=1);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def to_backendinfo(self):
        '''A tuple: (to_javaip, to_javaname)'''
        sql="select av_vmip,av_domainname from %s where sysid in (select ar_tovmid from %s where ar_zoneid='%s' and ar_typeid=1);" % (VMTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

    def portidinfo(self):
        '''A tuple: (portid, to_portid) int'''
        sql="select ar_portid,ar_toportid from %s where ar_zoneid='%s' and ar_typeid=1;" % (ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0]

#####################################################################################
    def hefu_baoliu(self):
        ''' 合服保留区区号 int'''
        if not self.hefu_zones(): return ''
        return min(self.hefu_zones())

    def hefu_zones(self):
        '''合服关系: list: [int,int,int ...]'''
        sql="select ab_zoneid from %s where ab_dbname=(select ab_dbname from %s where ab_zoneid='%s');" % (GAMETABLE,GAMETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return [int(i[0]) for i in session.execute(sql).fetchall()]    #a list

    def gameinfo(self):
        '''A tuple: (前端域名、前端ip、对外id、开服时间、autoid、联运商id) '''
        sql="select ab_fronthost,ab_frontip,ab_outid,ab_opentime,ab_autoid,ab_transportid from %s where ab_zoneid='%s';" % (GAMETABLE,self.num)
        res=session.execute(sql).fetchall()   # a  tuple
        if not res: return ''
        return res[0]

    def socketport(self):
        '''int'''
        sql="select ap_game from %s where sysid=(select ar_portid from %s where ar_zoneid='%s' and ar_typeid=1);" % (PORTTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0][0]

    def to_socketport(self):
        '''int'''
        sql="select ap_game from %s where sysid=(select ar_toportid from %s where ar_zoneid='%s' and ar_typeid=1);" % (PORTTABLE,ROLETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0][0]


    def timezone(self):
        sql="select ab_timezone from %s where ab_zoneid='%s'" % (GAMETABLE,self.num)
        res=session.execute(sql).fetchall()
        if not res: return ''
        return res[0][0]


class gameinfo_summarize(object):
    def allzone(self):
        #A set
        sql='select ab_zoneid from %s where ab_normal <> -1' % GAMETABLE
        res=session.execute(sql).fetchall()
        return set([i[0] for i in res])-no_update_zone    #所有正式服(去掉2095、9999、9998)

    def all_baoliu(self):
        allzone_baoliu=set()
        for num in self.allzone():
            ins=cmdbinfo(num)
            # print num,str(num)==str(ins.hefu_baoliu())
            if str(num)==str(ins.hefu_baoliu()): allzone_baoliu.add(num)   # 跳过合服区
        return allzone_baoliu

    def get_baoliu(self,nums,skiphefu):
        new=set()
        if skiphefu:
            for num in nums:
                ins=cmdbinfo(num)
                # print num,str(num)==str(ins.hefu_baoliu())
                if str(num)==str(ins.hefu_baoliu()): new.add(num)   # 跳过合服区
        else:
            for num in nums:
                ins=cmdbinfo(num)
                if ins.hefu_baoliu(): new.add(str(ins.hefu_baoliu()))  #不跳过合服区(将合服主区加入)
        return new



if __name__=='__main__':
    try:
        aa=cmdbinfo(sys.argv[1])
        print aa.dbinfo()          # dbip        dbport
        print aa.slaveinfo()       # slaveip     slaveport     slavepassword
        print aa.to_dbinfo()       # to_dbip     to_dbport
        print aa.to_slaveinfo()    # to_slaveip, to_slaveport, to_slavepassword
        print aa.dbnameinfo()      # dbname,     to_dbname
        print aa.backendinfo()     # javaip,     javaname
        print aa.to_backendinfo()  # to_javaip,  to_javaname
        print aa.portidinfo()      # portid,     to_portid
        print aa.hefu_baoliu()
        print aa.hefu_zones()
        print aa.gameinfo()
        print aa.socketport()
        print aa.to_socketport()
        print aa.timezone()
    except :
        print aa
        errinfo()

    print '=========================='
    someinfo=gameinfo_summarize()
    print someinfo.all_baoliu()


# (u'10.143.82.136', 3306L)
# (u'10.143.84.113', 3306L, u'')
# (u'10.143.82.136', 3306L)
# (u'10.143.84.113', 3306L, u'')
# (u'yxzg_1', u'yxzg_1')
# (u'10.143.78.155', u'203.195.161.52')
# (u'10.143.78.155', u'203.195.161.52')
# (1L, 1L)
# 1
# [1, 2, 3]  # int
# (u'10.221.149.20', u'10.221.149.20', 3L, 1407477600L, 10003L, u'373700003')
# 8003
# 8003
# -2   #u'-2' unicode
