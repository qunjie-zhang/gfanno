import time

class Log:
    def __init__(self):
        pass
    def info(self,msg = '',workname='Default'):
        now = time.asctime( time.localtime(time.time()))
        print(f'{now} - {workname}: {msg}')

    def debug(self,msg = '',workname='Default'):
        now = time.asctime( time.localtime(time.time()))
        print(f'{now} - [DEBUG]: {msg}')

    def notice(self,msg = '',workname='Default'):
        now = time.asctime( time.localtime(time.time()))
        print(f'{now} - {workname}: [ {msg} ]')

    def error_info(self,msg = ''):
        now = time.asctime( time.localtime(time.time()))
        print(f'{now} - [Error]: {msg}')
        # print('Please use [-h] to get more help!')

    def record(self,log_file_path,args,result):
        with open(log_file_path,'a',encoding='utf8') as file:
            file.write(f'Activate Time: {time.asctime( time.localtime(time.time()))} \n')
            file.write(f'Command: {args} \n')
            file.write('--'*25 +'\n')
            file.write(result+'\n')
            file.write('==' * 25 +'\n')
        return True
