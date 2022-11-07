name = ["Lena", 22, "Jonas", 26, "Anna", 27, "Kalle", 23, "Erik", 30, "Josefine", 20, "Emelie", 32, "Johanna", 29,
    "Peter", 19]
name2 = ["denis", 18, "Lena", 22]
name.extend(name2)
def name_age(name):
    dic = {}
    age = 0
    for n in range(0, len(name), 2):
        dic[name[n]] = name[n+1]
    for i in dic:
        print (i, dic[i])
        age = age + dic[i]
    avg_age = age / len(dic)
    return avg_age
name_age(name)