from Bio import pairwise2
from datetime import datetime


with open('matpeptide.txt','r') as file:
    matpeptide = file.read().replace('\n','')
    matpeptide = matpeptide.replace(' ','')
    matpeptide = matpeptide.upper()


with open('humangenome.txt','r') as file2:
    humangenome = file2.read()
    humangenome = humangenome.upper()


startTime=datetime.now()
alignments = pairwise2.align.localxx(humangenome, matpeptide)
for alignment in alignments:
    print(pairwise2.format_alignment(*alignment))
alignmenttime = datetime.now() - startTime

print("Running time for local alignment is ", alignmenttime)

