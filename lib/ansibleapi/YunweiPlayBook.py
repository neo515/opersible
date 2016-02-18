#coding=utf-8
# from ansible.playbook.play import Play
from ansible.playbook import PlayBook
from ansible.utils.template import template

from ansible import callbacks
import pprint
import ansible
import json

class YunweiPlayBook(PlayBook):
    """ 自定义PlayBook class"""
    def __init__(self, *args, **kwargs):
        self.rsfile = kwargs.pop('rsfile', None)
        super(YunweiPlayBook, self).__init__(*args, **kwargs)

    def _save_task_results(self, task_results):
        #对task_results做一个判断，看是success_output还是error_output
        # if task_results['dark']:
        #     AnsibleTask.objects.create(error_output=json.dumps(task_results))
        # else:
        #     AnsibleTask.objects.create(success_output=json.dumps(task_results))

        # {'dark': {}, 'contacted': {u'moban_upjava_10': {'msg': u'hehe', 'verbose_always': True, 'invocation': {'module_name': 'debug', 'module_args': "msg='hehe'"}}}}

        # print 'result: ',task_results
        # pprint.pprint(task_results)
        logfile=open(self.rsfile,'a+')
        print >>logfile,task_results
        # print >>logfile, "%s \t %s "
        logfile.close()

    def _run_task(self, play, task, is_handler):
        ''' run a single task in the playbook and recursively run any subtasks.  '''

        ansible.callbacks.set_task(self.callbacks, task)
        ansible.callbacks.set_task(self.runner_callbacks, task)

        if task.role_name:
            name = '%s | %s' % (task.role_name, task.name)
        else:
            name = task.name

        self.callbacks.on_task_start(template(play.basedir, name, task.module_vars, lookup_fatal=False, filter_fatal=False), is_handler)
        if hasattr(self.callbacks, 'skip_task') and self.callbacks.skip_task:
            ansible.callbacks.set_task(self.callbacks, None)
            ansible.callbacks.set_task(self.runner_callbacks, None)
            return True

        # load up an appropriate ansible runner to run the task in parallel
        results = self._run_task_internal(task)
        #在这里直接把结果存进数据库
        self._save_task_results(results)

        # if no hosts are matched, carry on
        hosts_remaining = True
        if results is None:
            hosts_remaining = False
            results = {}

        contacted = results.get('contacted', {})
        self.stats.compute(results, ignore_errors=task.ignore_errors)

        # add facts to the global setup cache
        for host, result in contacted.iteritems():
            if 'results' in result:
                # task ran with_ lookup plugin, so facts are encapsulated in
                # multiple list items in the results key
                for res in result['results']:
                    if type(res) == dict:
                        facts = res.get('ansible_facts', {})
                        self.SETUP_CACHE[host].update(facts)
            else:
                facts = result.get('ansible_facts', {})
                self.SETUP_CACHE[host].update(facts)
            # extra vars need to always trump - so update  again following the facts
            self.SETUP_CACHE[host].update(self.extra_vars)
            if task.register:
                if 'stdout' in result and 'stdout_lines' not in result:
                    result['stdout_lines'] = result['stdout'].splitlines()
                self.SETUP_CACHE[host][task.register] = result

        # also have to register some failed, but ignored, tasks
        if task.ignore_errors and task.register:
            failed = results.get('failed', {})
            for host, result in failed.iteritems():
                if 'stdout' in result and 'stdout_lines' not in result:
                    result['stdout_lines'] = result['stdout'].splitlines()
                self.SETUP_CACHE[host][task.register] = result

        # flag which notify handlers need to be run
        if len(task.notify) > 0:
            for host, results in results.get('contacted',{}).iteritems():
                if results.get('changed', False):
                    for handler_name in task.notify:
                        self._flag_handler(play, template(play.basedir, handler_name, task.module_vars), host)

        ansible.callbacks.set_task(self.callbacks, None)
        ansible.callbacks.set_task(self.runner_callbacks, None)
        return hosts_remaining
