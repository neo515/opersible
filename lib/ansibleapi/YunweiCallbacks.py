from ansible.callbacks import PlaybookCallbacks,PlaybookRunnerCallbacks

class MyPlaybookCallbacks(PlaybookCallbacks):
    ''' playbook.py callbacks used by /usr/bin/ansible-playbook '''
    # def __init__(self, verbose=False):
    #     super(MyPlaybookCallbacks,self).__init(self,verbose=False)
    def on_start(self):
        pass
    def on_notify(self, host, handler):
        pass
    def on_no_hosts_matched(self):
        pass
    def on_no_hosts_remaining(self):
        pass
    def on_task_start(self, name, is_conditional):
        pass
    def on_vars_prompt(self, varname, pr):
        pass
    def on_setup(self):
        pass
    def on_import_for_host(self, host, imported_file):
        pass
    def on_not_import_for_host(self, host, missing_file):
        pass
    def on_play_start(self, pattern):
        pass
    def on_stats(self, stats):
        pass



class MyPlaybookRunnerCallbacks(PlaybookRunnerCallbacks):
    def on_ok(self, host, host_result):
        pass
