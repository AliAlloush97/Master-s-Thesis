from pyJoules.energy_meter import measure_energy
from Bio import pairwise2
from datetime import datetime
from pyJoules.handler.csv_handler import CSVHandler

startTime=datetime.now()

csv_handler = CSVHandler('result.csv')


@measure_energy(handler=csv_handler)

def foo():
    with open('matpeptide.txt','r') as file:
        matpeptide = file.read().replace('\n','').replace(' ','').upper()


    with open('wuhan.txt','r') as file2:
        wuhan = file2.read().replace('\n','').replace(' ','').upper()

    alignments = pairwise2.align.globalxx(wuhan, matpeptide)
    for alignment in alignments:
        print(pairwise2.format_alignment(*alignment))
    alignmenttime = datetime.now() - startTime
    print("Running time for global alingment is ", alignmenttime)

for i in range(1):
	foo()
csv_handler.save_data()