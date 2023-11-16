from Bio import AlignIO

alignment = AlignIO.read(open("SEED.txt"), "stockholm")

print(alignment)

