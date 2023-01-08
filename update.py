def key_changer(dict_1):
    for key in dict_1.keys():
        x = key
        break
    dict_1.pop(x)
    return (dict_1)

if __name__ == "__main__":
    tl = 10
    my_dict = {(0, 0, 150) : 10, (0, 0, 0) : 2, (0, 150, 0) : 3, 
        (150, 0, 0) : 4, (0, 0, 152) : 1, (0, 149, 0) : 1}
    dict_1 = dict(my_dict)
    duplicate = {}
    for key in my_dict.keys():
        dict_1 = key_changer(dict_1)
        for keys,values in dict_1.items():
            r = abs(key[0]-keys[0])
            g = abs(key[1]-keys[1])
            b = abs(key[2]-keys[2])
            if r <= tl and g <= tl and b <= tl:
                my_dict[key] += dict_1[keys]
                duplicate[keys] = values
    for keys,values in duplicate.items():
        my_dict.pop(keys)

    print (my_dict)