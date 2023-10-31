class Fasta:
    def __init__(self):
        pass
    def load(self,fasta_path):
        with open(fasta_path, 'r', encoding='utf8') as f:
            f = f.readlines()
            seq_name = None
            seq = None
            for line in f:
                if not line: break
                if line.startswith('>'):
                    if seq:
                        yield seq_name, seq
                    seq = ''
                    seq_name = line[1:].strip('\n')
                else:
                    seq += line.strip('\n')
            yield seq_name, seq

    def load_dict(self,fasta_path):
        fasta_dict = dict()
        for i in self.load(fasta_path):
            fasta_dict[i[0]] = i[1]
        return fasta_dict

    # �жϵ�������
    def is_protein_sequence(sequence):
        amino_acids = "ACDEFGHIKLMNPQRSTVWY"
        # ��������Ƿ�ֻ������������ĸ
        return all(aa in amino_acids for aa in sequence.upper())

    def is_nucleic_acid_sequence(sequence):
        nucleotides = "ACGT"
        # ��������Ƿ�ֻ���������ĸ
        return all(base in nucleotides for base in sequence.upper())



