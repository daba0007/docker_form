#!/usr/bin/env python
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

def ansible_playbook(playbook):
    """
    执行一个playbook
    """
    Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                          'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                          'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check', 'diff'])
    loader = DataLoader()                                                                                       # 创建一个变量管理器
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                      module_path=None, forks=100, remote_user='slotlocker', private_key_file=None,
                      ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                      become_method=None, become_user='root', verbosity=None, check=False, diff=False)      # 定义参数
    passwords = dict(vault_pass='secret')                                                                     # 定义密码
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])                             # 定义一个inventory及hosts文件位置(/etc/ansible/hosts)
    variable_manager = VariableManager(loader=loader, inventory=inventory)                                     # 定义变量管理器
    playbook = PlaybookExecutor(playbooks=[playbook], inventory=inventory, variable_manager=variable_manager, loader=loader,
                            options=options, passwords=passwords)                                              # 定义一个playbook
    playbook.run()                                                                                             # 执行playbook
