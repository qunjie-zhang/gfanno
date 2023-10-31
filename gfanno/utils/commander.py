import os,subprocess
from . import log

class commander:
    def __init__(self,log_path=None):
        if log_path == None:
            self.log_path = os.path.join(os.getcwd(),'Command.log')
        else:
            self.log_path = log_path

    # 执行命令
    def cmd(self,command):
        subp = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
        return subp

    def run(self,command,record=False):
        res = self.cmd(command,)
        if record:
            l = log.Log()
            l.record(log_file_path=self.log_path,args=res.args,result=res.stdout)
        # 如果状态码不为了则Error
        res.check_returncode()
        return res

