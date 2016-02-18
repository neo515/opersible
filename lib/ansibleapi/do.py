#coding=utf-8

####### 具体请参考ansible-playbook文件 #######
from ansible import utils   #
from ansible import errors  #
from ansible import callbacks
from YunweiCallbacks import MyPlaybookCallbacks,MyPlaybookRunnerCallbacks
import os,sys,traceback,time

from ansible.callbacks import display
from ansible.color import ANSIBLE_COLOR, stringc


from YunweiPlayBook import YunweiPlayBook
# from ansible.playbook import PlayBook


# from ansible.inventory import Inventory

from YunweiInventory import YunweiInventory


def errinfo():
    time.sleep(0.2)
    aaa=sys.exc_info()
    traceback.print_exception(aaa[0],aaa[1],aaa[2])

def get_inventory(adict):#,yunwei_vars)
    # Inventory默认使用 ``ANSIBLE_HOSTS``
    inventory = YunweiInventory(adict) #, yunwei_vars=yunwei_vars)
    if len(inventory.list_hosts()) == 0:
        raise errors.AnsibleError("provided hosts list is empty")
    return inventory

def get_playbook(ymlfile):
    '''返回一个yml文件路径'''
    #return settings.TEMP_PLAYBOOK_PATH
    return ymlfile

def get_sudo():
    return False

def get_sudo_user():
    return 'root'

# 全局变量
stats = callbacks.AggregateStats()

# ``PlaybookCallbacks`` 是用来写结果到console的, ``PlaybookRunnerCallbacks``也是用来写结果到console。
# playbook_cb = MyPlaybookCallbacks(verbose=True) #verbose=utils.VERBOSITY)
# runner_cb = callbacks.DefaultRunnerCallbacks() #(stats, verbose=utils.VERBOSITY)

################
#开启调试信息输出
playbook_cb = callbacks.PlaybookCallbacks(verbose=True)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=True) #两个参数，不同于DefaultRunnerCallbacks
# runner_cb = MyPlaybookRunnerCallbacks(stats, verbose=True) #两个参数，不同于DefaultRunnerCallbacks
################

def hostcolor(host, stats, color=True):
    if ANSIBLE_COLOR and color:
        if stats['failures'] != 0 or stats['unreachable'] != 0:
            return "%-37s" % stringc(host, 'red')
        elif stats['changed'] != 0:
            return "%-37s" % stringc(host, 'yellow')
        else:
            return "%-37s" % stringc(host, 'green')
    return "%-26s" % host

def colorize(lead, num, color):
    """ Print 'lead' = 'num' in 'color' """
    if num != 0 and ANSIBLE_COLOR and color is not None:
        return "%s%s%-15s" % (stringc(lead, color), stringc("=", color), stringc(str(num), color))
    else:
        return "%s=%-4s" % (lead, str(num))

def job(ymlfile,adict,rsfile):  #data_dict
    playbook_path = get_playbook(ymlfile)
    # 设置playbook目录
    inventory = get_inventory(adict )#,data_dict)
    inventory.set_playbook_basedir(os.path.dirname(playbook_path))
    '''
    print 'remote_user:',type(options.remote_user),repr(options.remote_user)  #远程用户 <type 'str'>
    print 'remote_pass:',type(sshpass),repr(sshpass)    #远程用户密码  <type 'str'>
    print 'sudo:',type(options.sudo),repr(options.sudo) #是否使用sudo <type 'bool'>
    print 'sudo_user:',type(options.sudo_user),repr(options.sudo_user) #sudo用户 <type 'str'>
    print 'sudo_pass:',type(sudopass),repr(sudopass)    #sudo密码  <type 'NoneType'>
    print 'su:',type(options.su),repr(options.su)       #是否使用su  <type 'bool'>
    print 'su_pass:',type(su_pass),repr(su_pass)        #su密码  <type 'NoneType'>
    print 'su_user:',type(options.su_user),repr(options.su_user) #su密码 <type 'str'>
    '''

    pb = YunweiPlayBook(
        playbook=playbook_path,
        inventory=inventory,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        sudo=get_sudo(),
        #yunwei_task=yunwei_task,
        rsfile=rsfile,
        # remote_user='ansibleuser',
        # remote_pass='nWrjcUZzoyvP',
        # sudo_user='root',
        # sudo_pass=None
        )

    failed_hosts = []
    unreachable_hosts = []

    # 运行pb，然后使用返回的数据
    # try:
    # pb.run()直接写结果到console
    ansible_res=pb.run()
    # print ansible_res
    hosts = sorted(pb.stats.processed.keys())
    display(callbacks.banner("PLAY RECAP"))
    playbook_cb.on_stats(pb.stats)

    for h in hosts:
        t = pb.stats.summarize(h)
        if t['failures'] > 0:
            failed_hosts.append(h)
        if t['unreachable'] > 0:
            unreachable_hosts.append(h)

    retries = failed_hosts + unreachable_hosts

    # if len(retries) > 0:
    #     filename = pb.generate_retry_inventory(retries)
    #     if filename:
    #         display("           to retry, use: --limit @%s\n" % filename)
    #         raise RuntimeError('ansible error')

    for h in hosts:
        t = pb.stats.summarize(h)

        display("%s : %s %s %s %s" % (
            hostcolor(h, t),
            colorize('ok', t['ok'], 'green'),
            colorize('changed', t['changed'], 'yellow'),
            colorize('unreachable', t['unreachable'], 'red'),
            colorize('failed', t['failures'], 'red')),
            screen_only=True
        )

        display("%s : %s %s %s %s" % (
            hostcolor(h, t, False),
            colorize('ok', t['ok'], None),
            colorize('changed', t['changed'], None),
            colorize('unreachable', t['unreachable'], None),
            colorize('failed', t['failures'], None)),
            log_only=True
        )

    print ""
    # if len(failed_hosts) > 0:
    #     return ansible_res
    # if len(unreachable_hosts) > 0:
    #     return ansible_res

    # except errors.AnsibleError, e:
    #     # errinfo
    #     display("ERROR: %s" % e, color='red')
    #     return ansible_res
    # else:
    return ansible_res
