# -*- coding:utf-8 -*-
import json
from connect.ansible_api import AnsibleAPI



class AnsiInterface(AnsibleAPI):
    def __init__(self, resource, *args, **kwargs):
        super(AnsiInterface, self).__init__(resource, *args, **kwargs)

    @staticmethod
    def deal_result(info):
        host_ips = info.get('success').keys()
        info['success'] = host_ips

        error_ips = info.get('failed')
        error_msg = {}
        for key, value in error_ips.items():
            temp = {}
            temp[key] = value.get('stderr')
            error_msg.update(temp)
        info['failed'] = error_msg
        return json.dumps(info)

    def copy_file(self, host_list, src=None, dest=None):
        """
        copy file
        """
        module_args = "src=%s  dest=%s"%(src, dest)

        self.run(host_list, 'copy', module_args)
        result = self.get_result()
        return self.deal_result(result)

    def exec_command(self, host_list, cmds):
        """
        commands
        """
        self.run(host_list, 'command', cmds)
        result = self.get_result()
        return self.deal_result(result)

    def exec_script(self, host_list, path):
        """
        在远程主机执行shell命令或者.sh脚本
        """
        self.run(host_list, 'shell', path)
        result = self.get_result()
        return self.deal_result(result)



#if __name__ == "__main__":
 #   resource = [{"hostname": "192.168.0.106", "port": "22", "username": "root", "password": "password", "ip": '192.168.0.106'},
  #              {"hostname": "192.168.0.108", "port": "22", "username": "root", "password": "password", "ip": '192.168.0.108'}]
  #  interface = AnsiInterface(resource)
  #  print("copy: %s" % (interface.copy_file(['192.168.0.106', '192.168.0.108'], src='/home/test.py', dest='/home')))
    #print "commands: ", interface.exec_command(['172.20.3.18', '172.20.3.31'], 'hostname')
    #print "shell: ", interface.exec_script(['172.20.3.18', '172.20.3.31'], 'chdir=/home ls')
    #print "shell: ", interface.exec_script(['172.20.3.18', '172.20.3.31'], 'sh /opt/test.sh')