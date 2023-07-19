
with open('humangenome.txt', 'r') as file1:
    splitgenome = file1.read(500000)
    
with open('humangenomesplit.txt', 'w') as file2:
    file2.write(splitgenome)
