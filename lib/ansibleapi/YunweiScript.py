#coding=utf-8
from ansible.inventory.script import InventoryScript

class YwScript(InventoryScript):
    '''重写了类的方法'''
    def __init__(self,adict):
        self.data = adict
        # see comment about _meta below
        self.host_vars_from_top = None
        self.groups = self._parse('')

    def get_host_variables(self, host):
        if self.host_vars_from_top is not None:
            got = self.host_vars_from_top.get(host.name, {})
            return got

