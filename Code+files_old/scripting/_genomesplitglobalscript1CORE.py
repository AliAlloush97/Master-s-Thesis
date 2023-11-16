from pyJoules.energy_meter import measure_energy
from Bio import pairwise2
from datetime import datetime
from pyJoules.handler.csv_handler import CSVHandler
import os
import psutil

def restrict_to_single_core():
    pid = os.getpid()
    current_affinity = psutil.Process(pid).cpu_affinity()
    new_affinity = [1]
    psutil.Process(pid).cpu_affinity(new_affinity)

restrict_to_single_core()

startTime=datetime.now()

csv_handler = CSVHandler('genomesplitglobalsinglecore.csv')


@measure_energy(handler=csv_handler)

def foo():
    with open('humangenomesplit.txt','r') as file:
        humangenomesplit = file.read().replace('\n','').replace(' ','').upper()


    with open('matpeptide.txt','r') as file2:
        matpeptide = file2.read().replace('\n','').replace(' ','').upper()

    alignments = pairwise2.align.globalxx(humangenomesplit, matpeptide)
    for alignment in alignments:
        print(pairwise2.format_alignment(*alignment))
    alignmenttime = datetime.now() - startTime
    print("Running time for global alingment is ", alignmenttime)

for i in range(1):
	foo()
csv_handler.save_data()