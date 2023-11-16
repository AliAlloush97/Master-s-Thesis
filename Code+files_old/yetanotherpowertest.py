from pyJoules.device.nvidia_device import NvidiaGPUDomain
from Bio import pairwise2
from datetime import datetime

startTime=datetime.now()


with EnergyContext(domains=[NvidiaGPUDomain(0)]):
    def foo():
        with open('matpeptide.txt','r') as file:
            matpeptide = file.read().replace('\n','')
            matpeptide = matpeptide.replace(' ','')
            matpeptide = matpeptide.upper()


        with open('wuhan.txt','r') as file2:
            wuhan = file2.read()

        alignments = pairwise2.align.localxx(wuhan, matpeptide)
        for alignment in alignments:
            print(pairwise2.format_alignment(*alignment))
        alignmenttime = datetime.now() - startTime
        print("Running time for local alingment is ", alignmenttime)



foo()