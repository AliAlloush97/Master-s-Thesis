with open('matpeptide.txt','r') as file:
    matpeptide = file.read().replace('\n','')
    matpeptide = matpeptide.replace(' ','')
    matpeptide = matpeptide.upper()
print (matpeptide)

with open('wuhan.txt','r') as file2:
    wuhan = file2.read()
print (wuhan)