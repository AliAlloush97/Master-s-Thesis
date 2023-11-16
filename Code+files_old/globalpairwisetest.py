from Bio import pairwise2
from datetime import datetime


with open('matpeptide.txt','r') as file:
    matpeptide = file.read().replace('\n','').replace(' ','').upper()

with open('wuhan.txt','r') as file2:
    wuhan = file2.read().replace('\n','').replace(' ','').upper()


startTime=datetime.now()
alignments = pairwise2.align.globalxx(wuhan, matpeptide)
for alignment in alignments:
    print(pairwise2.format_alignment(*alignment))
alignmenttime = datetime.now() - startTime
print("Running time for global alingment is ", alignmenttime)