import getopt
import os
import shutil
import sys
import time
from .GeneFamilyAnno import GeneFamilyAnno
from .utils.config import config
from .utils.fasta import Fasta
from .utils.log import Log
from decimal import Decimal

__VERSION__ = '1.4'

def help_command():
    msg = f'''Program:    gfanno (Gene Family Annoation Workflow)
Version:    {__VERSION__}

    Useage: gfanno  <command> [options]

    Commands:
        -f / --fasta        Input fasta file path. This option is required.
        -- / --deredundant  To de-redundant the annotation results of different subfamilies.
                            Enter at least two gfanno output files,Suppy ort - o parameter to specifoutput name.
        -o / --output       Output file path.
        -c / --config       Use the specified configuration file. This parameter is optional. 
                            If you do not set this parameter, the program will use 'gfanno_config.ini' by default.
        -t / --target       Specifies the parameter category used in the configuration file. This option is required.
        -g / --generate     Generate the default configuration file (gfanno_config.ini) under the current path.
                            Used to initialize the software operating environment or reset damaged configuration files.
        -- / --data         Release built-in data sets in the current directory.
        -h / --help         Display this help message.
        -v / --version      Detailed version information.
        '''
    print(msg)
    exit()

def version_command():
    msg = f'''gfanno {__VERSION__}\nCopyright (C) 2023 Bioinformatics Laboratory of South China Agricultural University.'''
    print(msg)
    exit()

# 输出示例文件
def dataset_init_command():
    hmm_data = os.path.join(os.path.dirname(__file__), 'dataset', 'hmm')
    seed_data = os.path.join(os.path.dirname(__file__), 'dataset', 'seed')
    try:
        print("Releasing sample data files to default destination folder...")
        shutil.copytree(hmm_data, 'hmm')
        shutil.copytree(seed_data, 'seed')
        print('Successful operation!')
        exit()
    except FileExistsError as e:
        print(e)
        exit(1)


# 生成配置文档
def generate_config_command():
    cfg = config('gfanno_config.ini')
    cfg.config_init()
    log = Log()
    log.info('Configuration file has been recreated: gfanno_config.ini')
    exit()


# 输出 stat 文件
def write_state(path, fasta_path, config_info, filter_res):
    table_header = '# Target_ID\t\tb_iden\tb_qcov\tb_tcovs\t' + '\t'.join(
        [i + '_coverage' for i in config_info['domain'].split(',')])
    with open(path, 'w', encoding='utf8') as state_file:
        state_file.write('# Gfanno state output\n')
        state_file.write('# -----------------------\n')
        state_file.write(f"# Date:{time.asctime()}\n")
        state_file.write(f"# Fasta:{os.path.basename(fasta_path)}\n")
        state_file.write(f"# Seed:{os.path.basename(config_info['blastp_seed'])}\n")
        state_file.write(f"# Hmm model:{config_info['hmm']}\n")
        state_file.write(f"# Domain:{os.path.basename(config_info['domain'])}\n")
        state_file.write(f"# b_iden:{config_info['b_iden']}\n")
        state_file.write(f"# b_qcov:{config_info['b_qcov']}\n")
        state_file.write(f"# b_tcov_limit: {config_info['b_tcov_min']}--{config_info['b_tcov_max']}\n")
        state_file.write(f"# h_cov:{config_info['h_cov']}\n")
        state_file.write('\n' + table_header + '\n')
        for id, value in filter_res.items():
            state_file.write(
                f"{id}\t{round(float(value['identity']))}\t{round(float(value['b_qcov']))}\t{round(float(value['b_tcovs']))}\t" + '\t'.join(
                    [str(round(float(value['domain'][i]))) for i in config_info['domain'].split(',')]) + '\n')

# 多个文件合并去冗余
# S:version1.4
# 2024.3.19 wangzt
def deredundant(output_path='merge.stat', merge_file_list=[]):
    l = Log()
    l.info('de-redundant multiple stat files..')
    # 初始化一个domain命令。
    domain = ''
    table_header = ''

    # 创建一个字典  id：内容列表
    file_dict = dict()

    for file in merge_file_list:
        if not os.path.exists(file):
            l.error_info('File does not exist： ' + file)
            exit(1)

        with open(file,'r',encoding='utf8') as f:
            f = f.read().splitlines()
            for line in f:

                # 验证数据表格列
                if line.startswith('# Target_ID'):
                    if table_header == '':
                        table_header = line
                    else:
                        if table_header != line:
                            print(merge_file_list[0] + '\t->\t' + table_header)
                            print(file + '\t->\t' + line)
                            l.error_info('Inconsistent data table structure!')
                            exit(1)

                # 验证 domain 数量及顺序
                if line.startswith('# Domain:'):
                    if domain == '':
                        domain = line
                    else:
                        if domain != line:
                            print(merge_file_list[0] + '\t->\t' + domain[2:])
                            print(file + '\t->\t' + line[2:])
                            l.error_info('Domain name or order is inconsistent!')
                            exit(1)

                if line.startswith('#') or line.strip(' ') == '':continue
                line = line.split('\t')

                if line[0] not in file_dict:
                    file_dict[line[0]] = line
                else:
                    if int(line[1]) > int(file_dict[line[0]][1]):
                        file_dict[line[0]] = line

    with open(output_path,'w',encoding='utf8') as w:
        w.write('# Gfanno state file deredundant output\n')
        w.write('# --------------------------------\n')
        w.write(f"# Date: {time.asctime()}\n")
        w.write(f"# File list: {','.join(merge_file_list)}\n")
        w.write('\n' + table_header + '\n')
        for k,v in file_dict.items():
            w.write('\t'.join(v) + '\n')
    l.info('Done.')

def main():
    # Log
    log = Log()
    # 初始化默认输入参数
    fasta_path = False
    # 去冗余文件列表
    deredundant_file_list = False

    config_path = 'gfanno_config.ini'
    config_target = False
    output_path = 'output'
    DEBUG = False


    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'hvVf:o:c:gt:',
                                   ['help', 'version', 'fasta=', 'output=', 'config=', 'generate', 'deredundant=','data', 'target:','debug'])
    except getopt.GetoptError as e:
        log.error_info(e)
        exit(1)

    if opts == []: help_command()

    for opt_name, opt_value in opts:
        # 即时结束类参数
        if opt_name in ('-h', '--help'):
            help_command()
        if opt_name in ('-v', '-V', '--version'):
            version_command()
        if opt_name in ('--data'):
            dataset_init_command()
        if opt_name in ('-g', '--generate'):
            generate_config_command()
        # 定义配置文件
        if opt_name in ('-c', '--config'):
            config_path = opt_value.strip()
        # 定义配置文件模板参数目标
        if opt_name in ('-t', '--target'):
            config_target = opt_value.strip()
        if opt_name in ('-f', '--fasta'):
            fasta_path = opt_value.strip()
        if opt_name in ('-o', '--output'):
            output_path = opt_value.strip()

        if opt_name in ('--deredundant'):
            deredundant_file_list = opt_value.strip().split(',')

        if opt_name in ('--debug'):
            DEBUG = True


    # 判断本次是否进行合并操作
    if deredundant_file_list != False:
        deredundant(output_path,deredundant_file_list)
        exit()


    log.info(f'Current configuration file used: {config_path}')
    if not os.path.exists(config_path):
        log.error_info(
            f'The specified configuration file \'{config_path}\' does not exist!\nPlease use [-h] to generate a new config file!')
        exit(1)

    # 实例化config，核查配置文件信息
    cfg = config(config_path)
    check_res = cfg.config_check_missing()

    # 如果配置文件存在错误，则check变量为列表，循环显示错误信息并结束程序
    if check_res != True:
        for i in check_res:
            log.error_info(i)
        print('\nPlease try to fix the above error prompts or create a new configuration file to use!')
        exit(1)

    # 总配置文件 获取全部配置信息
    config_info_all = cfg.config_getinfo()
    # 执行配置文件.将所需要的配置数据拷贝到该字典中，后续循环执行该字典内容
    config_info = dict()


    # 正常计算流程

    if fasta_path == False or not os.path.exists(fasta_path):
        log.error_info('Please check the fasta file path information!')
        exit(1)

    # 解析Fasta文件
    fa = Fasta()
    fasta_dict = fa.load_dict(fasta_path)

    # 如果没有指定 -t 参数，则将 全部 配置文件信息 交付 执行字典
    if config_target == False:
        log.info('All configuration parameters will be executed!')
        config_info = config_info_all
    else:
        log.info(f'The specified configuration parameters will be executed: {config_target}')
        config_target = config_target.split(',')

        for target in config_target:
            if target in config_info_all:
                config_info[target] = config_info_all[target]
            else:
                log.error_info(
                    f"The target '{target}' does not exist. Please check whether the configuration file is correct.")
                exit(1)

    BASE_DIR = os.getcwd()
    OUTPUT_DIR = output_path
    WORKSPACE_ROOT_DIR = os.path.join(BASE_DIR, 'Gfanno_Workspace')
    LOG_PATH = os.path.join(WORKSPACE_ROOT_DIR, 'log.txt')

    if not os.path.exists(OUTPUT_DIR): os.mkdir(OUTPUT_DIR)
    if not os.path.exists(WORKSPACE_ROOT_DIR): os.mkdir(WORKSPACE_ROOT_DIR)

    s = GeneFamilyAnno(debug=DEBUG)

    # 根据执行配置文件数量进行循环
    for target_name, target_info in config_info.items():
        log.info(f'Currently in progress: {os.path.basename(fasta_path)} --> [{target_name}]')
        if DEBUG:
            log.debug(f'Target name: {target_name}')
            log.debug(f'Target info: {target_info}')

        # target_info
        #  {'blastp_seed': 'seed/4CL.seed.fasta',
        #  'hmm': 'hmm/AMP-binding_C.hmm',
        #  'domain': 'AMP-binding_C',
        #  'b_iden': '50',
        #  'b_qcov': '50',
        #  'h_cov': '50'}

        # 输出路径的子目录名称
        sub_prefix = os.path.basename(fasta_path).split('.')[0] + '_' + target_name
        output_fasta_path = os.path.join(OUTPUT_DIR, sub_prefix + '_seq')
        # 创建fasta输出目录
        if not os.path.exists(output_fasta_path):
            os.mkdir(output_fasta_path)

        workflow_res = s.run(
            workspace_path=WORKSPACE_ROOT_DIR,
            fasta_path=fasta_path,
            seed_path=target_info['blastp_seed'],
            hmm_path_list=target_info['hmm'].split(',')
        )
        # workflow_res = {'
        # blastp_out': '/home/wangzt/GeneFamilyAnno/Gfanno_Workspace/TGY_PPO_1698500660/blastp.out',
        # 'hmm_out': '/home/wangzt/GeneFamilyAnno/Gfanno_Workspace/TGY_PPO_1698500660/hmm.out',
        # 'fasta': 'TGY.pro.fasta',
        # 'hmm': ['hmm/PPO1_DWL.hmm', 'hmm/PPO1_KFDV.hmm']}

        if DEBUG:
            log.debug('Workflow_res')
            print(workflow_res)

        hmmout_path = workflow_res['hmm_out']
        blastpout_path = workflow_res['blastp_out']

        # 处理传入多个domain域 与 h_cov 值
        domain_list = target_info['domain'].split(',')
        h_cov = target_info['h_cov'].split(',')

        b_iden = Decimal(target_info['b_iden'])
        b_qcov = Decimal(target_info['b_qcov'])
        
        b_tcov_max = Decimal(target_info['b_tcov_max'])
        b_tcov_min = Decimal(target_info['b_tcov_min'])

        # # 在检查配置文件时检查该项目
        # if len(domain) != len(h_cov):
        #     exit('Domain 数量 与 h_cov 参数数量不一致！')

        # domain域：h_cov值
        domain_coverage = dict()

        if DEBUG:
            log.debug(f'domain_list: {domain_list}')
            log.debug(f'h_cov: {h_cov}')

        for d, p in zip(domain_list, h_cov):
            domain_coverage[d] = Decimal(p)
        if DEBUG:
            log.debug(f'Domain <-> h_cov: {domain_coverage}')

        # hmm file
        # {'TGY|GWHPASIV043514': {'domain': {'Prenyltrans': 93.18, 'SQHop_cyclase_C': 99.06, 'SQHop_cyclase_N': 90.72}}
        hmm_file_filter_dict = dict()
        # 创建参数未过滤版本，用于输出全部信息
        hmm_file_nofilter_dict = dict()

        # 将满足数值过滤条件数据添加进字典
        with open(hmmout_path, 'r', encoding='utf8') as hmmout_file:
            hmmout_file = hmmout_file.read().splitlines()

            for line in hmmout_file:
                if line.startswith('#'): continue
                line = line.split()

                line_h_cov_compute = round(((Decimal(line[16]) - Decimal(line[15])) / Decimal(line[5])) * 100,2)  # 保留两位小数
                line_domain = line[3]
                line_evalue = Decimal(line[6])

                if DEBUG:
                    log.debug(
                        f'h_cov: {line_domain} SET:{domain_coverage[line_domain]}  COMPUTE:{line_h_cov_compute}')

                # 当前行domain在 domain列表内：
                if line_domain in domain_coverage:

                    # 2024.3.25 因需要输出全部信息包含被过滤信息，此处创建新的未过滤字典
                    # 创建参数未过滤版本 evalue值进行限制
                    if line_evalue < 1E-10:
                        if line[0] not in hmm_file_nofilter_dict:
                            hmm_file_nofilter_dict[line[0]] = {
                                'domain': {
                                    line_domain: line_h_cov_compute
                                }
                            }
                        else:
                            # 当前 ID 已在列表中
                            #  如果当前 domin 不存在 或 已存在值小于目标 则a进行更新操作
                            if line_domain not in hmm_file_nofilter_dict[line[0]]['domain'] or hmm_file_nofilter_dict[line[0]]['domain'][line_domain] < line_h_cov_compute:
                                hmm_file_nofilter_dict[line[0]]['domain'][line_domain] = line_h_cov_compute


                    # 创建参数过滤版本
                    if line_h_cov_compute > domain_coverage[line_domain] and line_evalue < 1E-10:
                    # 当前 ID 不在列表中
                        if line[0] not in hmm_file_filter_dict:
                            hmm_file_filter_dict[line[0]] = {
                                'domain': {
                                    line_domain: line_h_cov_compute
                                }
                            }
                        else:
                            # 当前 ID 已在列表中
                            #  如果当前 domin 不存在 或 已存在值小于目标 则a进行更新操作
                            if line_domain not in hmm_file_filter_dict[line[0]]['domain'] or hmm_file_filter_dict[line[0]]['domain'][line_domain] < line_h_cov_compute:
                                hmm_file_filter_dict[line[0]]['domain'][line_domain] = line_h_cov_compute

        if DEBUG:
            log.debug(f'hmm_file_filter_dict 1: {hmm_file_filter_dict}')
            log.debug(f'hmm_file_nofilter_dict 1: {hmm_file_nofilter_dict}')

        # 设置多个domain域时需同时满足，此处剔除达标数量足的数据
        del_list = list()
        for id, dm in hmm_file_filter_dict.items():
            for d in domain_coverage:
                if d not in dm['domain']:
                    del_list.append(id)
                    break
        for id in del_list:
            del hmm_file_filter_dict[id]

        # 2024.3.25 因需要输出全部信息包含被过滤信息
        del_list.clear()
        for id, dm in hmm_file_nofilter_dict.items():
            for d in domain_coverage:
                if d not in dm['domain']:
                    del_list.append(id)
                    break
        for id in del_list:
            del hmm_file_nofilter_dict[id]

        if DEBUG:
            log.debug(f'hmm_file_filter_dict 2: {hmm_file_filter_dict}')
            log.debug(f'hmm_file_nofilter_dict 2: {hmm_file_nofilter_dict}')

        seed_dict = fa.load_dict(target_info['blastp_seed'])

        # blastpout_file_filter_dict()
        # {id:{identity,b_qcov}}

        # Blastp 数据过滤
        blastpout_file_filter_dict = dict()
        # Blastp 数据未过滤
        blastpout_file_nofilter_dict = dict()

        with open(blastpout_path, 'r', encoding='utf8') as blastpout_file:
            blastpout_file = blastpout_file.read().splitlines()
            for line in blastpout_file:

                # 对blastp输出信息进行过滤，剔除容易造成错误的数据
                if line.startswith('Warning'):continue
                if line.startswith('FASTA-Reader'):continue
                line = line.split()
                if len(line) != 13:continue

                line_id = line[0]
                seed_id = line[1]
                try:
                    line_b_iden = Decimal(line[2])
                    line_evalue = Decimal(line[10])
                    line_b_qcov = Decimal(line[12])
                    line_b_tcovs = int(Decimal(line_b_qcov) * len(fasta_dict[line_id]) / len(seed_dict[seed_id]))
                except:
                    log.error_info('Type conversion error: There is abnormal information in the blast output file')
                    print(line)
                    exit(1)
                
                # b_tcov limit
                # Fix Bug: 2024.3.25 超过最大值时应定义为最大值
                # if line_b_tcovs > b_tcov_max: line_b_tcovs = b_tcov_min
                if line_b_tcovs > b_tcov_max: line_b_tcovs = b_tcov_max
                if line_b_tcovs < b_tcov_min: line_b_tcovs = b_tcov_min

                # Blastp 仅过滤evalue后输出至 数据未过滤 分组
                if line_evalue < 1E-10:
                    if line_id not in blastpout_file_nofilter_dict:
                        blastpout_file_nofilter_dict[line_id] = {
                            'identity': line_b_iden,
                            'b_qcov': line_b_qcov,
                            'b_tcovs': line_b_tcovs
                        }
                    else:
                        if blastpout_file_nofilter_dict[line_id]['identity'] < line_b_iden:
                            blastpout_file_nofilter_dict[line_id]['identity'] = line_b_iden
                            blastpout_file_nofilter_dict['b_qcov'] = line_b_qcov
                            blastpout_file_nofilter_dict[line_id]['b_tcovs'] = line_b_tcovs
                        else:
                            pass


                # Blastp 数据过滤
                if line_evalue < 1E-10 and line_b_iden >= b_iden and line_b_qcov > b_qcov:
                    # 当前 ID 不存在该列表
                    if line_id not in blastpout_file_filter_dict:
                        blastpout_file_filter_dict[line_id] = {
                            'identity': line_b_iden,
                            'b_qcov': line_b_qcov,
                            'b_tcovs': line_b_tcovs
                        }
                    else:
                        # # 如果已存在则进行判断后决定是否替换
                        # # 每个值均为独立不关联状态
                        # if blastpout_file_filter_dict[line_id]['identity'] < line_b_iden:
                        #     blastpout_file_filter_dict[line_id]['identity'] = line_b_iden
                        # if blastpout_file_filter_dict[line_id]['b_qcov'] < line_b_qcov:
                        #     blastpout_file_filter_dict['b_qcov'] = line_b_qcov
                        # if blastpout_file_filter_dict[line_id]['b_tcovs'] < line_b_tcovs:
                        #     blastpout_file_filter_dict[line_id]['b_tcovs'] = line_b_tcovs

                        # 如果已存在则进行判断后决定是否替换
                        # 取Blastp最大值那一行
                        # 如果记录值小于当前行，则进行替换操作
                        if blastpout_file_filter_dict[line_id]['identity'] < line_b_iden:
                            blastpout_file_filter_dict[line_id]['identity'] = line_b_iden
                            blastpout_file_filter_dict['b_qcov'] = line_b_qcov
                            blastpout_file_filter_dict[line_id]['b_tcovs'] = line_b_tcovs

            #     if line_evalue < 1E-10 and line_b_iden >= b_iden and line_b_qcov > b_qcov:
            #         # 当前 ID 不存在该列表
            #         if line_id not in blastpout_file_filter_dict:
            #             blastpout_file_filter_dict[line_id] = list()
            #             blastpout_file_filter_dict[line_id].append({
            #                 'identity': line_b_iden,
            #                 'b_qcov': line_b_qcov,
            #                 'b_tcovs': line_b_tcovs,
            #                 #  当传入多个hmm模型时则会出现多个h_cov值，此处取出现的最小值用于后续排序
            #                 # 'hmm_low_coverage':min([y for x,y in hmm_file_filter_dict[line_id]['domain'].items()])
            #             })
            #         else:
            #             blastpout_file_filter_dict[line_id].append({
            #                 'identity': line_b_iden,
            #                 'b_qcov': line_b_qcov,
            #                 'b_tcovs': line_b_tcovs,
            #                 # 'hmm_low_coverage': min([y for x, y in hmm_file_filter_dict[line_id]['domain'].items()])
            #             })
            #
            # print('=='*20)
            # print(blastpout_file_filter_dict)
            # exit()

        # print(hmm_file_filter_dict)
        # print(blastpout_file_filter_dict)

        # {'TGY|GWHPASIV043514': {'domain': {'Prenyltrans': 93.18, 'SQHop_cyclase_C': 99.06, 'SQHop_cyclase_N': 90.72}}, 'TGY|GWHPASIV031780': {'domain': {'Prenyltrans': 90.91, 'SQHop_cyclase_C': 98.43, 'SQHop_cyclase_N': 96.91}}}
        # {'TGY|GWHPASIV009143': {'identity': 94.751, 'b_qcov': 100.0}, 'TGY|GWHPASIV015605': {'identity': 95.333, 'b_qcov': 100.0}, 'TGY|GWHPASIV031776': {'identity': 100.0, 'b_qcov': 100.0}, 'TGY|GWHPASIV031777': {'identity': 94.882, 'b_qcov': 99.0}, 'TGY|GWHPASIV031780': {'identity': 96.133, 'b_qcov': 100.0}}

        filter_res = dict()
        for hmm_id in hmm_file_filter_dict:
            if hmm_id in blastpout_file_filter_dict:
                filter_res[hmm_id] = {
                    'identity': blastpout_file_filter_dict[hmm_id]['identity'],
                    'b_qcov': blastpout_file_filter_dict[hmm_id]['b_qcov'],
                    'b_tcovs': blastpout_file_filter_dict[hmm_id]['b_tcovs'],
                    'domain': hmm_file_filter_dict[hmm_id]['domain']
                }

        nofilter_res = dict()
        for hmm_id in hmm_file_nofilter_dict:
            if hmm_id in blastpout_file_nofilter_dict:
                nofilter_res[hmm_id] = {
                    'identity': blastpout_file_nofilter_dict[hmm_id]['identity'],
                    'b_qcov': blastpout_file_nofilter_dict[hmm_id]['b_qcov'],
                    'b_tcovs': blastpout_file_nofilter_dict[hmm_id]['b_tcovs'],
                    'domain': hmm_file_nofilter_dict[hmm_id]['domain']
                }


        # filter_res =   {'TGY|GWHPASIV025623': {'identity': 65.587, 'b_qcov': 99.0, 'domain': {'PPO1_DWL': 98.08, 'PPO1_KFDV': 99.23}}, 'TGY|GWHPASIV025620': {'identity': 61.497, 'b_qcov': 94.0, 'domain': {'PPO1_DWL': 98.08, 'PPO1_KFDV': 99.23}}, 'TGY|GWHPASIV026886': {'identity': 74.769, 'b_qcov': 73.0, 'domain': {'PPO1_DWL': 96.15, 'PPO1_KFDV': 98.46}}}

        write_state(path=os.path.join(OUTPUT_DIR, sub_prefix + '.stat'), fasta_path=fasta_path, config_info=target_info,
                    filter_res=filter_res)

        write_state(path=os.path.join(OUTPUT_DIR, sub_prefix + '.all.stat'), fasta_path=fasta_path, config_info=target_info,
                    filter_res=nofilter_res)


        for seq_name in filter_res.keys():
            with open(os.path.join(output_fasta_path, seq_name + '.fasta'), 'w', encoding='utf8') as fa_file:
                fa_file.write(f'>{seq_name}\n')
                fa_file.write(fasta_dict[seq_name] + '\n')

    # if not DEBUG:
    #     s.clean(WORKSPACE_ROOT_DIR)
    log.info('Done.')


if __name__ == '__main__':
    main()
