# operansible
利用ansible结合cmdb开发的运维自动化系统

本系统用于运维维护更新公司所有项目/平台的游戏。
本系统更像是一个框架；对应不同的游戏，只需要添加相应的配置或代码即可。
底层使用了游戏对应的cmdb系统。

实现了： 操作一些游戏服/区，只需要填入区号，接着执行python run.py即可，简化了运维的工作。

├─config     #该系统需要用到的一些配置，如cmdb连接信息等
├─config_an  #ansible程序使用到的一些配置文件
├─lib        #库：读取cmdb 、 调用ansible api
├─logs
└─tasks      #该目录下以目录存放着每个task。每个task是建立在ansible程序之上
    └─setup_game   #setup_game task， 用于部署游戏服， 
        ├─project
        └─roles    #ansible-playbook的roles
        
