#coding=utf-8

HouTais={
    'ytyytengxun':{                      # 名字格式: GAME_NAME+PLATFORM
        'comment':'英雄联盟',
        'CMDB_IP':'1.2.3.4',             # cmdb数据库信息
        'CMDB_PORT':'12345',
        'CMDB_NAME':'gameweb',
        'CMDB_USER':'game',
        'CMDB_PASSWD':'nihao_20120926',
        'VMTABLE':'gsys_admin_vm',
        'ROLETABLE':'gsys_admin_role',
        'GAMETABLE':'gsys_admin_db',
        'PORTTABLE':'gsys_admin_port',
        'sqls':     [
                    #'some sqls;'
                    ],
        'no_update_zone':set([99999,2000,2001]),    #全服更新时跳过这些服
        'separate_zone':'16',                       #分批更新分界点: 目前来说英雄联盟为16,   王者荣耀为11, 不分批更新为空值
        'autoid_suffix_lenght':11                   #除去前缀的autoid之后的位数, 如autoid为1001, 则实际是100100000000001
    }
}


LOGFILE='/data/work/logs/ansiblework.log'

