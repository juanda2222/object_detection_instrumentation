cString = '1Hola2Mundo3p4c5sd6jaja7...8:D9-0'
nString = ''
for i in cString:
    if (i >= chr(48)) and (i <= chr(57)):
       nString += i
print(nString)