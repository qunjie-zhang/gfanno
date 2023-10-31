import configparser
import os.path


# 用于配置文件的操作

class config:
    def __init__(self,filename='gfanno_config.ini'):
        # 实例化 configparser 为 cfg
        self.cfg = configparser.ConfigParser()
        self.filename=filename

        # 默认必须配置项
        self.default_required_options = ['blastp_seed','hmm','domain','blastp_identity','blastp_qcovs','hmm_coverage']
        # 默认文件配置参参数
        self.default_file_options = ['blastp_seed','hmm']

    # 初始化配置文件内容
    def config_init(self):

        self.cfg['4CL'] = {
            'blastp_seed': "seed/4CL.seed.fasta",
            'hmm': "hmm/AMP-binding_C.hmm",
            'domain': "AMP-binding_C",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '50',
        }
        self.cfg['ANR'] = {
            'blastp_seed': "seed/ANR.seed.fasta",
            'hmm': "hmm/Epimerase.hmm",
            'domain': "Epimerase",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['ANS'] = {
            'blastp_seed': "seed/ANS.seed.fasta",
            'hmm': "hmm/csp2OGD.hmm",
            'domain': "csp2OGD",
            'blastp_identity': '60',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['C4H'] = {
            'blastp_seed': "seed/C4H.seed.fasta",
            'hmm': "hmm/cspCYP450.hmm",
            'domain': "cspCYP450",
            'blastp_identity': '60',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['CHI'] = {
            'blastp_seed': "seed/CHI.seed.fasta",
            'hmm': "hmm/Chalcone.hmm",
            'domain': "Chalcone",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['CHS'] = {
            'blastp_seed': "seed/CHS.seed.fasta",
            'hmm': "hmm/Chal_sti_synt_C.hmm",
            'domain': "Chal_sti_synt_C",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['DFR'] = {
            'blastp_seed': "seed/DFR.seed.fasta",
            'hmm': "hmm/Epimerase.hmm",
            'domain': "Epimerase",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['F33H'] = {
            'blastp_seed': "seed/F33H.seed.fasta",
            'hmm': "hmm/cspCYP450.hmm",
            'domain': "cspCYP450",
            'blastp_identity': '70',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['F3H'] = {
            'blastp_seed': "seed/F3H.seed.fasta",
            'hmm': "hmm/csp2OGD.hmm",
            'domain': "csp2OGD",
            'blastp_identity': '50',
            'blastp_qcovs': '60',
            'hmm_coverage': '60',
        }
        self.cfg['F35H'] = {
            'blastp_seed': "seed/F35H.seed.fasta",
            'hmm': "hmm/cspCYP450.hmm",
            'domain': "cspCYP450",
            'blastp_identity': '60',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['FLS'] = {
            'blastp_seed': "seed/FLS.seed.fasta",
            'hmm': "hmm/csp2OGD.hmm",
            'domain': "csp2OGD",
            'blastp_identity': '60',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['FNSII'] = {
            'blastp_seed': "seed/FNSII.seed.fasta",
            'hmm': "hmm/cspCYP450.hmm",
            'domain': "cspCYP450",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['LAR'] = {
            'blastp_seed': "seed/LAR.seed.fasta",
            'hmm': "hmm/NmrA.hmm",
            'domain': "NmrA",
            'blastp_identity': '40',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['PAL'] = {
            'blastp_seed': "seed/PAL.seed.fasta",
            'hmm': "hmm/Lyase_aromatic.hmm",
            'domain': "Lyase_aromatic",
            'blastp_identity': '70',
            'blastp_qcovs': '50',
            'hmm_coverage': '60',
        }
        self.cfg['PPO'] = {
            'blastp_seed': "seed/PPO.seed.fasta",
            'hmm': "hmm/PPO1_DWL.hmm,hmm/PPO1_KFDV.hmm",
            'domain': "PPO1_KFDV,PPO1_DWL",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '70,70',
        }
        self.cfg['SCPL1A'] = {
            'blastp_seed': "seed/SCPL1A.seed.fasta",
            'hmm': "hmm/Peptidase_S10.hmm",
            'domain': "Peptidase_S10",
            'blastp_identity': '40',
            'blastp_qcovs': '50',
            'hmm_coverage': '70',
        }
        self.cfg['UGT84A'] = {
            'blastp_seed': "seed/UGT84A.seed.fasta",
            'hmm': "hmm/UDPGT.hmm",
            'domain': "UDPGT",
            'blastp_identity': '50',
            'blastp_qcovs': '50',
            'hmm_coverage': '20',
        }
        self.cfg['LDOX'] = {
            'blastp_seed': "seed/LDOX.seed.fasta",
            'hmm': "hmm/csp2OGD.hmm",
            'domain': "csp2OGD",
            'blastp_identity': '60',
            'blastp_qcovs': '50',
            'hmm_coverage': '70',
        }

        with open(self.filename, 'w',encoding='utf8') as configfile:
            configfile.write(';This configuration files used by Gfanno\n;You can refer to the configuration method in the sample file to add the configuration you need.\n\n')
            configfile.write(";The ‘hmm’, ‘domain’, ‘hmm_coverage’ can all support the input of multiple parameters, and use ',' to separate the parameters.\n")
            configfile.write(";'hmm_coverage' corresponds to the 'hmm' parameter, and the number of these two parameters needs to be kept consistent.\n\n")
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

        # k 为配置文件种的列表名称
        for config_list_name in selections:
            # if k == 'global':continue

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
                if len(self.cfg.get(config_list_name,'hmm').split(',')) != len(self.cfg.get(config_list_name,'hmm_coverage').split(',')):
                    error_list.append(f"The number of HMM models is inconsistent with the number of HMM_COVERAGE parameters: '{config_list_name}' at '{self.filename}'")

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