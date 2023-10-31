import pandas as pd
'''
   ______  ________    _     Gene Family Annotation Pipline                           
 .' ___  ||_   __  |  / \     Bioinformatics Lab of SCAU.            
/ .'   \_|  | |_ \_| / _ \     _ .--.   _ .--.   .--.   
| |   ____  |  _|   / ___ \   [ `.-. | [ `.-. |/ .'`\ \ 
\ `.___]  |_| |_  _/ /   \ \_  | | | |  | | | || \__. | 
 `._____.'|_____||____| |____|[___||__][___||__]'.__.'  
---------------------------------------------------------------------- 
'''
class filter:
    def __init__(self):
        pass
    def extract_candidate_gene(self,hmmfile, blastpfile, domain, pfam_coverage, identity, blastp_qcovs, fileout):
        identity = int(identity)
        blastp_qcovs = int(blastp_qcovs)
        pfam_coverage = int(pfam_coverage)

        hmm_file = pd.read_csv(hmmfile, sep='\s+', comment='#', header=None)
        hmm_file[17] = ((hmm_file.iloc[:, 16] - hmm_file.iloc[:, 15]) / hmm_file.iloc[:, 5]) * 100
        hmm_evalue = hmm_file[hmm_file.iloc[:, 6] < 1E-10]
        hmm_subset = hmm_evalue.iloc[:, [0, 3, 17]]
        hmm_subset.columns = ['target_id', 'domain', 'pfam_coverage_handle']

        hmm_coverage = hmm_subset[hmm_subset['pfam_coverage_handle'] >= pfam_coverage]
        # Split the data into+ two parts based on domain.
        domains = domain.split(',')
        df_list = []
        for d in domains:
            df_list.append(hmm_coverage[hmm_coverage['domain'] == d])

        for id, pd_domain in enumerate(df_list):
            if id == 0:
                hmm_domain = df_list[0]
                continue
            else:
                hmm_domain = pd.merge(pd_domain, hmm_domain, on='target_id', how='inner')

        blastp_file = pd.read_csv(
            blastpfile,
            sep='\t', header=None, usecols=[0, 2, 10, 12],
            names=['target_id', 'blastp_identity', 'evalue', 'blastp_qcovs'])
        blastp_evalue = blastp_file[blastp_file['evalue'] < 1E-10]
        blastp_identity = blastp_evalue[blastp_evalue['blastp_identity'] >= identity]
        blastp_qcovs = blastp_identity[blastp_identity['blastp_qcovs'] >= blastp_qcovs]

        merged_hmm_blastp = pd.merge(hmm_domain, blastp_qcovs, on='target_id')
        df = merged_hmm_blastp.sort_values(by=['blastp_identity'], ascending=[False])
        df2 = df.drop_duplicates(subset=['target_id'], keep='first')


        df2.insert(loc=0,column='pfam_coverage',value=pfam_coverage)

        df_out = df2[['target_id','blastp_identity','blastp_qcovs','pfam_coverage']]
        df_out.to_csv(fileout, index=False)