
class Filter:
    def __init__(self):
        pass

    def run(self,seed_path,hmmout_path,blastpout_path,domain_list,hmm_coverage,blastp_identity,blastp_qcovs):

        # 处理传入多个domain域 与 hmm_coverage 值
        domain = domain_list.split(',')
        hmm_coverage = hmm_coverage.split(',')

        # # 在检查配置文件时检查该项目
        # if len(domain) != len(hmm_coverage):
        #     exit('Domain 数量 与 hmm_coverage 参数数量不一致！')

        # 初始化参数类型
        blastp_identity = float(blastp_identity)
        blastp_qcovs = float(blastp_qcovs)

        # domain域：hmm_coverage值
        domain_coverage = dict()
        for d, p in zip(domain, hmm_coverage):
            domain_coverage[d] = float(p)
        # print('Domain <--> hmm_coverage')
        # print(domain_coverage)

        # hmm file
        # {'TGY|GWHPASIV043514': {'domain': {'Prenyltrans': 93.18, 'SQHop_cyclase_C': 99.06, 'SQHop_cyclase_N': 90.72}}
        hmm_file_filter_dict = dict()

        # 将满足数值过滤条件数据添加进字典
        with open(hmmout_path, 'r', encoding='utf8') as hmmout_file:
            hmmout_file = hmmout_file.read().splitlines()

            for line in hmmout_file:
                if line.startswith('#'): continue
                line = line.split()

                line_hmm_coverage_compute = round(((float(line[16]) - float(line[15])) / float(line[5])) * 100,
                                                  2)  # 保留两位小数
                line_domain = line[3]
                line_evalue = float(line[6])

                if line_domain in domain_coverage and line_hmm_coverage_compute > domain_coverage[
                    line_domain] and line_evalue < 1E-10:
                    # 当前 ID 不在列表中
                    if line[0] not in hmm_file_filter_dict:
                        hmm_file_filter_dict[line[0]] = {
                            'domain': {
                                line_domain: line_hmm_coverage_compute
                            }
                        }
                    else:
                        # 当前 ID 已在列表中
                        #  如果当前 domain 不存在 或 已存在值小于目标 则进行更新操作
                        if line_domain not in hmm_file_filter_dict[line[0]]['domain'] or \
                                hmm_file_filter_dict[line[0]]['domain'][line_domain] < line_hmm_coverage_compute:
                            hmm_file_filter_dict[line[0]]['domain'][line_domain] = line_hmm_coverage_compute

        # 设置多个domain域时需同时满足，此处剔除不满足数据
        del_list = list()
        for id, dm in hmm_file_filter_dict.items():
            for d in domain_coverage:
                if d not in dm['domain']:
                    del_list.append(id)
                    break
        for id in del_list:
            del hmm_file_filter_dict[id]

        # blastpout_file_filter_dict()
        # {id:{identity,blastp_qcovs}}
        blastpout_file_filter_dict = dict()
        with open(blastpout_path, 'r', encoding='utf8') as blastpout_file:
            blastpout_file = blastpout_file.read().splitlines()
            for line in blastpout_file:
                line = line.split()

                line_id = line[0]
                line_blastp_identity = float(line[2])
                line_evalue = float(line[10])
                line_blastp_qcovs = float(line[12])

                if line_evalue < 1E-10 and line_blastp_identity >= blastp_identity and line_blastp_qcovs > blastp_qcovs:
                    # 当前 ID 不存在该列表
                    if line_id not in blastpout_file_filter_dict:
                        blastpout_file_filter_dict[line_id] = {
                            'identity': line_blastp_identity,
                            'blastp_qcovs': line_blastp_qcovs
                        }
                    else:
                        # 如果已存在则进行判断后决定是否替换
                        if blastpout_file_filter_dict[line_id]['identity'] < line_blastp_identity:
                            blastpout_file_filter_dict[line_id]['identity'] = line_blastp_identity
                        if blastpout_file_filter_dict[line_id]['blastp_qcovs'] < line_blastp_qcovs:
                            blastpout_file_filter_dict['blastp_qcovs'] = line_blastp_qcovs

        # print(hmm_file_filter_dict)
        # print(blastpout_file_filter_dict)

        # {'TGY|GWHPASIV043514': {'domain': {'Prenyltrans': 93.18, 'SQHop_cyclase_C': 99.06, 'SQHop_cyclase_N': 90.72}}, 'TGY|GWHPASIV031780': {'domain': {'Prenyltrans': 90.91, 'SQHop_cyclase_C': 98.43, 'SQHop_cyclase_N': 96.91}}}
        # {'TGY|GWHPASIV009143': {'identity': 94.751, 'blastp_qcovs': 100.0}, 'TGY|GWHPASIV015605': {'identity': 95.333, 'blastp_qcovs': 100.0}, 'TGY|GWHPASIV031776': {'identity': 100.0, 'blastp_qcovs': 100.0}, 'TGY|GWHPASIV031777': {'identity': 94.882, 'blastp_qcovs': 99.0}, 'TGY|GWHPASIV031780': {'identity': 96.133, 'blastp_qcovs': 100.0}}

        result = dict()
        for hmm_id in hmm_file_filter_dict:
            if hmm_id in blastpout_file_filter_dict:
                result[hmm_id] = {
                    'identity': blastpout_file_filter_dict[hmm_id]['identity'],
                    'blastp_qcovs': blastpout_file_filter_dict[hmm_id]['blastp_qcovs'],
                    'domain': hmm_file_filter_dict[hmm_id]['domain']
                }

        # result = {'TGY|GWHPASIV031780': {'identity': 96.133, 'blastp_qcovs': 100.0, 'domain': {'Prenyltrans': 90.91, 'SQHop_cyclase_C': 98.43, 'SQHop_cyclase_N': 96.91}}}

        return result
