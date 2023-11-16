from Bio import AlignIO

alignment = AlignIO.read(open("SEED.txt"), "stockholm")

for align in alignment:
    print (align.seq)

