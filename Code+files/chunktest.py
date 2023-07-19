#imports

from Bio import pairwise2
from datetime import datetime


# opening genome file

with open('humangenome.txt','r') as file2:
    humangenome = file2.read()
    humangenome = humangenome.upper()


# opening peptide file
# modifying the file, removing spaces and lines and changing all to upper case

with open('matpeptide.txt','r') as file:
    matpeptide = file.read().replace('\n','')
    matpeptide = matpeptide.replace(' ','')
    matpeptide = matpeptide.upper()

# taking start time
startTime=datetime.now()

#setting chunk size to perform local alignment on chunks instead of full genomic sequence due to memory errors
chunk_size = 100000
for i in range(0, len(humangenome), chunk_size):
    chunk = humangenome[i:i+chunk_size]

    #beginning local alignment with no gap penalty
    alignments = pairwise2.align.localxx(chunk, matpeptide)


for alignment in alignments:
    print(pairwise2.format_alignment(*alignment))
# calculates time needed to run the operation
alignmenttime = datetime.now() - startTime

print("Running time for local alingment is ", alignmenttime)