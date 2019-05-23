from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: debug_failure
    type: aggregate 
    short_description: outputs failed tasks and all resource variables
    description:
        - Ansible callback plugin for collecting all failed task actions. 
          Outputs all environment and ansible variables from the tasks.
    requirements:
        - whitelisting in configuration
'''
from ansible import constants
from ansible.plugins.callback import CallbackBase
from ansible.utils.color import stringc
from ansible.utils.display import Display

import json

global_display = Display()

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.7
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'debug_failure'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        self._display = global_display
        self.playbook = ""
        super(CallbackModule, self).__init__()

    def _format_debug_message(self, key, message, error=False):
        msg = "{}: ".format(key) 
        if isinstance(message, dict):
            msg += json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')) + "\n"
        else:
            msg += "{}".format(message)

        if error:
            self._display.display(msg, color=constants.COLOR_ERROR)
        else:
            self._display.display(msg, color=constants.COLOR_CHANGED)


    """
    When a task fails, print debugging output
    Args:
        res TaskResult: The resulting data from a failed task. 
            res._task Task ansible/lib/playbook/task.py
            res._host Host ansible/lib/inventory/host.py
            res._result <dict>
    """
    def v2_runner_on_failed(self, res, ignore_errors=False):
        self._display.display("*************************FAILURE VARIABLES*************************", color=constants.COLOR_CHANGED)
        self.vars = self.playbook.get_variable_manager().get_vars(self.playbook)["hostvars"][res._host.get_name()]
        for k, v in sorted(self.vars.items()):
            if not k.startswith("ansible_") and k is not "groups":
                self._format_debug_message(k, v)

        self._display.display("*************************FAILURE HOST INFO*************************", color=constants.COLOR_ERROR)
        self._format_debug_message("Host information", res._host.get_magic_vars(), error=True)
        self._display.display("*************************FAILURE TASK INFO*************************", color=constants.COLOR_ERROR)
        self._format_debug_message("Task Name", res._task.get_name(), error=True)
        self._format_debug_message("Task information", res._result, error=True)


    """
    Get the playbook object on start. This allows reference to the variable manager.
    """
    def v2_playbook_on_play_start(self, playbook):
        self.playbook = playbook
