import configparser
import os.path


# 用于配置文件的操作

class config:
    def __init__(self,filename='gfanno_config.ini'):
        # 实例化 configparser 为 cfg
        self.cfg = configparser.ConfigParser()
        self.filename=filename

        # 默认必须配置项
        self.default_required_options = ['blastp_seed','hmm','domain','b_iden','b_qcov','h_cov','b_tcov_max','b_tcov_min']
        # 默认文件配置参参数,将检查文件是否存在
        self.default_file_options = ['blastp_seed','hmm']

    # 初始化配置文件内容
    def config_init(self):

        self.cfg['4CL'] = {
            'blastp_seed': "seed/4CL.seed.fasta",
            'hmm': "hmm/AMP-binding_C.hmm",
            'domain': "AMP-binding_C",
            'b_iden': '50',
            'b_qcov': '50',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'h_cov': '50',
        }
        self.cfg['C4H'] = {
            'blastp_seed': "seed/C4H.seed.fasta",
            'hmm': "hmm/cspCYP450.hmm",
            'domain': "cspCYP450",
            'b_iden': '60',
            'b_qcov': '50',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'h_cov': '60',
        }
        self.cfg['CHI'] = {
            'blastp_seed': "seed/CHI.seed.fasta",
            'hmm': "hmm/Chalcone.hmm",
            'domain': "Chalcone",
            'b_iden': '50',
            'b_qcov': '50',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'h_cov': '60',
        }
        self.cfg['CHS'] = {
            'blastp_seed': "seed/CHS.seed.fasta",
            'hmm': "hmm/Chal_sti_synt_C.hmm",
            'domain': "Chal_sti_synt_C",
            'b_iden': '50',
            'b_qcov': '50',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'h_cov': '60',
        }

        self.cfg['PPO'] = {
            'blastp_seed': "seed/PPO.seed.fasta",
            'hmm': "hmm/PPO1_DWL.hmm,hmm/PPO1_KFDV.hmm",
            'domain': "PPO1_KFDV,PPO1_DWL",
            'b_iden': '50',
            'b_qcov': '50',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'h_cov': '70,70',
        }
        self.cfg['SCPL1A'] = {
            'blastp_seed': "seed/SCPL1A.seed.fasta",
            'hmm': "hmm/Peptidase_S10.hmm",
            'domain': "Peptidase_S10",
            'b_iden': '40',
            'b_tcov_max': '100',
            'b_tcov_min': '0',
            'b_qcov': '50',
            'h_cov': '70',
        }


        with open(self.filename, 'w',encoding='utf8') as configfile:
            configfile.write(';This configuration files used by Gfanno\n;You can refer to the configuration method in the sample file to add the configuration you need.\n\n')
            configfile.write(";The ‘hmm’, ‘domain’, ‘h_cov’ can all support the input of multiple parameters, and use ',' to separate the parameters.\n")
            configfile.write(";'h_cov' corresponds to the 'hmm' parameter, and the number of these two parameters needs to be kept consistent.\n\n")
            self.cfg.write(configfile)

    # 解析当前配置文件
    def config_parser(self):
        return self.cfg.read(filenames=self.filename, encoding='utf8')

    # 返回当前配置文件所有列表
    def config_show(self):
        self.config_parser()
        return self.cfg.sections()

    # 检查配置文件缺失项目,正确返回 True，错误返回异常列表
    def config_check_missing(self):
        self.config_parser()
        selections = self.cfg.sections()

        error_list = list()

        if selections == []:
            error_list.append(f'The current configuration file is missing configuration selections！: {self.filename}')

        # config_list_name 为配置文件种的列表名称
        for config_list_name in selections:
            # if config_list_name == 'global':continue

            options = self.cfg.options(config_list_name)
            if options == []:
                error_list.append(f'Missing configuration options in {config_list_name}')
                break

            # d 为默认参数键名
            for default_required_options_name in self.default_required_options:
                if default_required_options_name not in options:
                    error_list.append(f"Missing necessary parameter '{default_required_options_name}' in custom parameter list '{config_list_name}' at '{self.filename}'")

            if error_list == []:
                # 当前面配置项均存在时再执行该项检查避免出错
                if len(self.cfg.get(config_list_name,'hmm').split(',')) != len(self.cfg.get(config_list_name,'h_cov').split(',')):
                    error_list.append(f"The number of HMM models is inconsistent with the number of h_cov parameters: '{config_list_name}' at '{self.filename}'")
                # 检查 t_cov_max 与 t_cov_min 的值大小关系
                if float(self.cfg.get(config_list_name,'b_tcov_min')) > float(self.cfg.get(config_list_name,'b_tcov_max')):
                    error_list.append(f"Parameter t_cov_max has a smaller value than t_cov_min: '{config_list_name}' at '{self.filename}'")

            for default_file_options_name in self.default_file_options:
                files = self.cfg.get(config_list_name,default_file_options_name).split(',')
                for file in files:
                    if not os.path.exists(file):
                        error_list.append(f"File Not Found: '{file}'  Error parameter '{default_required_options_name}' in custom parameter list '{config_list_name}' at '{self.filename}' ")


        if error_list == []:return True
        else:return error_list

    # 获取全部配置信息 解析为字典
    def config_getinfo(self):
        self.config_parser()
        selections = self.cfg.sections()
        res = dict()
        for k in selections:
            res[k] = dict()
            for i in self.cfg.options(k):
                res[k][i] = self.cfg.get(k,i)
        return res


# t = config()
# # t.config_init()
# r = t.config_check_missing()
# if r != True:
#     for i in r:
#         print(i)
# else:
#     print('Success')