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
            'blastp_seed': 'seed/4CL.seed.fasta',
            'hmm': 'hmm/AMP-binding_C.hmm,hmm/AMP-binding.hmm',
            'domain': 'AMP-binding_C,AMP-binding',
            'b_iden': '40',
            'b_tcov_max': '120',
            'b_tcov_min': '60',
            'b_qcov': '70',
            'h_cov': '90,90'
        }

        self.cfg['CHS'] = {
            'blastp_seed': 'seed/CHS.seed.fasta',
            'hmm': 'hmm/Chal_sti_synt_C.hmm,hmm/Chal_sti_synt_N.hmm',
            'domain': 'Chal_sti_synt_C,Chal_sti_synt_N',
            'b_iden': '50',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90,90'
        }

        self.cfg['PPO'] = {
            'blastp_seed': 'seed/PPO.seed.fasta',
            'hmm': 'hmm/PPO1_DWL.hmm,hmm/PPO1_KFDV.hmm',
            'domain': 'PPO1_DWL,PPO1_KFDV',
            'b_iden': '35',
            'b_tcov_max': '130',
            'b_tcov_min': '70',
            'b_qcov': '70',
            'h_cov': '90,90'
        }

        self.cfg['C4H'] = {
            'blastp_seed': 'seed/C4H.seed.fasta',
            'hmm': 'hmm/p450.hmm',
            'domain': 'p450',
            'b_iden': '70',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['CHI'] = {
            'blastp_seed': 'seed/CHI.seed.fasta',
            'hmm': 'hmm/Chalcone.hmm',
            'domain': 'Chalcone',
            'b_iden': '35',
            'b_tcov_max': '130',
            'b_tcov_min': '70',
            'b_qcov': '70',
            'h_cov': '90'
        }

        self.cfg['DFR'] = {
            'blastp_seed': 'seed/DFR.seed.fasta',
            'hmm': 'hmm/Epimerase.hmm',
            'domain': 'Epimerase',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['ANR'] = {
            'blastp_seed': 'seed/ANR.seed.fasta',
            'hmm': 'hmm/Epimerase.hmm',
            'domain': 'Epimerase',
            'b_iden': '55',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['ANS'] = {
            'blastp_seed': 'seed/ANS.seed.fasta',
            'hmm': 'hmm/2OG-FeII_Oxy.hmm,hmm/DIOX_N.hmm',
            'domain': '2OG-FeII_Oxy,DIOX_N',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90,90'
        }

        self.cfg['F33H'] = {
            'blastp_seed': 'seed/F33H.seed.fasta',
            'hmm': 'hmm/p450.hmm',
            'domain': 'p450',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['F3H'] = {
            'blastp_seed': 'seed/F3H.seed.fasta',
            'hmm': 'hmm/2OG-FeII_Oxy.hmm,hmm/DIOX_N.hmm',
            'domain': '2OG-FeII_Oxy,DIOX_N',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90,90'
        }

        self.cfg['F35H'] = {
            'blastp_seed': 'seed/F35H.seed.fasta',
            'hmm': 'hmm/p450.hmm',
            'domain': 'p450',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['FLS'] = {
            'blastp_seed': 'seed/FLS.seed.fasta',
            'hmm': 'hmm/2OG-FeII_Oxy.hmm,hmm/DIOX_N.hmm',
            'domain': '2OG-FeII_Oxy,DIOX_N',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90,90'
        }

        self.cfg['FNSII'] = {
            'blastp_seed': 'seed/FNSII.seed.fasta',
            'hmm': 'hmm/p450.hmm',
            'domain': 'p450',
            'b_iden': '55',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['LAR'] = {
            'blastp_seed': 'seed/LAR.seed.fasta',
            'hmm': 'hmm/NmrA.hmm',
            'domain': 'NmrA',
            'b_iden': '30',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '65',
            'h_cov': '90'
        }

        self.cfg['PAL'] = {
            'blastp_seed': 'seed/PAL.seed.fasta',
            'hmm': 'hmm/Lyase_aromatic.hmm',
            'domain': 'Lyase_aromatic',
            'b_iden': '60',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['SCPL4'] = {
            'blastp_seed': 'seed/SCPL4.seed.fasta',
            'hmm': 'hmm/Peptidase_S10.hmm',
            'domain': 'Peptidase_S10',
            'b_iden': '70',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['SCPL5'] = {
            'blastp_seed': 'seed/SCPL5.seed.fasta',
            'hmm': 'hmm/Peptidase_S10.hmm',
            'domain': 'Peptidase_S10',
            'b_iden': '70',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['UGT84A'] = {
            'blastp_seed': 'seed/UGT84A.seed.fasta',
            'hmm': 'hmm/UGTnew.hmm',
            'domain': 'UGT',
            'b_iden': '40',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90'
        }

        self.cfg['LDOX'] = {
            'blastp_seed': 'seed/LDOX.seed.fasta',
            'hmm': 'hmm/2OG-FeII_Oxy.hmm,hmm/DIOX_N.hmm',
            'domain': '2OG-FeII_Oxy,DIOX_N',
            'b_iden': '55',
            'b_tcov_max': '120',
            'b_tcov_min': '80',
            'b_qcov': '80',
            'h_cov': '90,90'
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