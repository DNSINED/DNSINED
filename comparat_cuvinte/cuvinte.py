with open(r"C:\Users\SAVAN\Desktop\espanol.txt") as file1:
    with open(r"C:\Users\SAVAN\Desktop\italiano.txt") as file2:
        same = set(file1).intersection(file2)

same.discard('\n')
contor = 0
for line in same:
    contor += 1
print(contor)
