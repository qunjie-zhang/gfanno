import time, os
from .utils.commander import commander
from .utils.log import Log

class GeneFamilyAnno:
    def __init__(self, debug=False):
        self.debug = debug

    def run(self,workspace_path,fasta_path,seed_path,hmm_path_list):

        # Define Directory
        PROJECT_DIR = os.path.join(workspace_path,os.path.basename(fasta_path).split('.')[0] +'_'+ os.path.basename(seed_path).split('.')[0] + '_' + str(int(time.time())))
        LOG_PATH = os.path.join(PROJECT_DIR, 'log.txt')
        CPU_COUNT = os.cpu_count()

        if not os.path.exists(PROJECT_DIR):
            os.mkdir(PROJECT_DIR)

        # 文件路径定义
        BLASTDB_PATH = os.path.join(PROJECT_DIR, "blastdb", os.path.basename(seed_path))
        BLASTP_PATH = os.path.join(PROJECT_DIR, 'blastp.out')
        HMMSEARCH_PATH = os.path.join(PROJECT_DIR, 'hmm.out')

        # 实例化
        cmd = commander(LOG_PATH)
        log = Log()

        # makeblastdb
        # log.info(msg='Start Makeblastdb...')
        res = cmd.run(f'makeblastdb -in {seed_path} -dbtype prot -out {BLASTDB_PATH}',record=self.debug)

        # BLASTP
        # log.info(msg='Start Blastp...')
        res = cmd.run(
            f'blastp -num_threads {CPU_COUNT} -db {BLASTDB_PATH} -query {fasta_path} -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -seg yes',record=self.debug)
        with open(BLASTP_PATH, 'w', encoding='utf8') as f:
            f.write(res.stdout)

        # hmmsearch
        # 因允许传入多个hmm模型，所以此处进行处理
        # 因需要产生多个hmmout文件，所以此处设置名称列表
        hmmout_part_list = []

        for idx,hmm in enumerate(hmm_path_list):
            hmmout_part_name = os.path.join(PROJECT_DIR, str(idx)+'.hmmout.part')
            hmmout_part_list.append(hmmout_part_name)
            # log.info(msg=f'Start hmmsearch [{hmm}]')
            res = cmd.run(f'hmmsearch --cpu {CPU_COUNT} --domtblout {hmmout_part_name} {hmm} {fasta_path}',record=self.debug)

        # log.info(msg='Merge hmmout files ...')
        with open(HMMSEARCH_PATH,'w',encoding='utf8') as hmm_merge:
            for hmm_part in hmmout_part_list:
                with open(hmm_part,'r',encoding='utf8') as hmm_part:
                    hmm_part = hmm_part.read().splitlines()
                    for line in hmm_part:
                        if line.startswith('#'):continue
                        hmm_merge.write(line +'\n')
        # log.info(msg='Workflow Done.')
        return{
            'blastp_out':BLASTP_PATH,
            'hmm_out':HMMSEARCH_PATH,
            'fasta':fasta_path,
            'hmm':hmm_path_list
        }

    def clean(self,workspace_path):
        cmd = commander()
        cmd.run(f'rm -rf {workspace_path}',record=False)




