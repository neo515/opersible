#coding=utf-8

import cmdbinfo as cmdb
from time import time,strftime,localtime

def handle(nums,adict):


    # for num in tools.donums(nums,skiphefu=skiphefu):
    for num in nums:
        eachone={}
        ins=cmdb.cmdbinfo(num)
        backendip,backendname =ins.backendinfo()
        dbip,dbport           =ins.dbinfo()
        dbname                =ins.dbnameinfo()[0]
        socketport            =ins.socketport()
        t,platforms           =ins.gameinfo()[3:6:2]
        opentime              =strftime('{{%Y,%m,%d},{%H,%M,%S}}.',localtime(t))
        allhefu               =ins.hefu_zones()
        hefunums              =','.join(['\'\\\"S%s\\\"\'' % i for i in allhefu])

        eachone[('backend_'+str(num))]={
            'num':num ,
            'ansible_ssh_host':backendip,
            'javaip':backendip,
            'javaname':backendname,
            'dbip':dbip,
            'dbport':dbport,
            'dbname':dbname,
            'platforms':platforms,
            'hefunums':hefunums,
            'opentime':opentime,
            'socketport':socketport}
        adict['setup_game']['hosts'].update(eachone)
    return adict
