#coding=utf-8
from ansible.inventory import Inventory
from YunweiScript import YwScript
from ansible import utils
import os

class YunweiInventory(Inventory):

    def __init__(self, adict):
        '''重写,传入自定义的字典'''

        # the host file file, or script path, or list of hosts
        # if a list, inventory data will NOT be loaded
        self.host_list = ''
        self.adict=adict

        # caching to avoid repeated calculations, particularly with
        # external inventory scripts.

        self._vars_per_host  = {}
        self._vars_per_group = {}
        self._hosts_cache    = {}
        self._groups_list    = {}
        self._pattern_cache  = {}

        # to be set by calling set_playbook_basedir by ansible-playbook
        self._playbook_basedir = None

        # the inventory object holds a list of groups
        self.groups = []

        # a list of host(names) to contain current inquiries to
        self._restriction = None
        self._also_restriction = None
        self._subset = None

        self.parser = YwScript(adict)

        self.groups = self.parser.groups.values()

        utils.plugins.vars_loader.add_directory(self.basedir(), with_subdir=True)
        self._vars_plugins = [ x for x in utils.plugins.vars_loader.all(self) ]
    def basedir(self):
        cwd = '.'
        return os.path.abspath(cwd)