#!/usr/bin/python
import hashlib
import sys
import time##todo remove performance benchmarks
try:
    shadowFilePath = sys.argv[1]#getting the shadow file path from command line args
except:#checking to see if the file was specifed
    print("Password file must be specified:(python [thisFile] [full/relative file path])")
    exit(1)
shadowFile = open(shadowFilePath,'r')
hashUserNameTupleList = list()
harderHashUserNameTupleList = list()
for line in shadowFile:#add usersnames and hashes to hashUserNameTupleList
    lineList = line.split(':')
    hashUserNameTupleList.append((lineList[1].strip(),lineList[0]))
shadowFile.close()
for hashUserNameTuple in hashUserNameTupleList:
    harderHashUserNameTupleList.append({hashUserNameTuple[0],hashUserNameTuple[1]})
#open passwordfile and check if we already have any hashes
passwordFile = open("./.sufferWhatTheyMust",'r')
offest = 0
for line in passwordFile:
    shadowCount = 0

    for hashUserNameTuple in hashUserNameTupleList:
        if(line.split(':')[0].upper() == hashUserNameTuple[0].upper()):
            if(offest == 0):
                print("Found previously cracked username(s)/passwords:")
            print(hashUserNameTuple[1] + ":" + line.split(':')[1])
            hashUserNameTupleList.pop(shadowCount)
            offest += 1
        shadowCount += 1
passwordFile.close()
passwordFile = open("./.sufferWhatTheyMust",'a')
#Start numbercracking
numpass = 0
print("Starting numberical crack")
startTime = time.time()
while numpass <= 9999 and len(hashUserNameTupleList) != 0:#four digit
    if(len(hashUserNameTupleList) == 0):
        break
    bytepass = str(numpass).zfill(4).encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this numpass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            passwordFile.write(str(hashedPass).upper() + ":" + str(numpass).zfill(4) + "\n" )
            hashUserNameTupleList.pop(shadowCount)
            # print(len(hashUserNameTupleList),"passwords left to crack")
        shadowCount += 1
    numpass += 1
numpass = 0
while numpass <= 99999 and len(hashUserNameTupleList) != 0:#five digit
    if(len(hashUserNameTupleList) == 0):
        break
    bytepass = str(numpass).zfill(5).encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this numpass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            passwordFile.write(str(hashedPass).upper() + ":" + str(numpass).zfill(5) + "\n" )
            hashUserNameTupleList.pop(shadowCount)
            # print(len(hashUserNameTupleList),"passwords left to crack")
        shadowCount += 1
    numpass += 1
numpass = 0
while numpass <= 999999 and len(hashUserNameTupleList) != 0:#six digit
    if(len(hashUserNameTupleList) == 0):
        break
    bytepass = str(numpass).zfill(6).encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this numpass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            passwordFile.write(str(hashedPass).upper() + ":" + str(numpass).zfill(6) + "\n" )
            hashUserNameTupleList.pop(shadowCount)
            # print(len(hashUserNameTupleList),"passwords left to crack")
        shadowCount += 1
    numpass += 1
endTime = time.time()
print("Finished cracking numerical passwords in %.2f seconds." % (endTime-startTime))
startTime = time.time()
print("Starting dictionary crack")
dictionaryFile = open("/usr/share/dict/words",'r')
fourCharDictList = list()
fiveCharDictList = list()
dictList = list()
startTime = time.time()
for word in dictionaryFile:##load up dictionarylists from file
    word = word.strip()
    dictList.append(word)
    if(len(word) == 4):
        fourCharDictList.append(word)
    elif(len(word) == 5):
        fiveCharDictList.append(word)
##crack four char words according to this rule:
#A four char word which gets the first letter capitalized and a 1 digit number appended
for word in fourCharDictList:
    if(len(hashUserNameTupleList) == 0):
        break
    for i in range(0,10):
        word = str(word[0].upper() + word[1:len(word)])
        bytepass = str(word+str(i)).strip().encode('utf-8')
        m = hashlib.md5()
        m.update(bytepass)
        hashedPass = m.hexdigest()
        shadowCount = 0
        for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
            if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this pass is a collison with user pass
                print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
                passwordFile.write(str(hashedPass).upper() + ":" + str(word+str(i)).strip() + "\n" )
                hashUserNameTupleList.pop(shadowCount)
            shadowCount += 1
##crack five char words according to this rule:
#A five char word with the letter 'e' in it which gets replaced with the digit 3. (words with 2 2's
#   treat as two separate words:sleep, sl3ep,and sle3p, but not sl33p).
for word in fiveCharDictList:
    if(len(hashUserNameTupleList) == 0):
        break
    word = word.lower()
    eCount = 0
    wordList = list()
    charCount = 0
    for char in word:
        if char.lower() == 'e':
            eCount += 1
            wordList.append(word[0:charCount] + '3' + word[charCount+1:len(word)])
        charCount += 1
    for passwd in wordList:
        bytepass = str(passwd).strip().encode('utf-8')
        m = hashlib.md5()
        m.update(bytepass)
        hashedPass = m.hexdigest()
        shadowCount = 0
        for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
            if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this pass is a collison with user pass
                print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
                passwordFile.write(str(hashedPass).upper() + ":" + str(passwd).strip() + "\n" )
                hashUserNameTupleList.pop(shadowCount)
                # print(len(hashUserNameTupleList),"passwords left to crack")
            shadowCount += 1
##crack all char words according to this rule:
#Any number of chars single word
for word in dictList:
    if(len(hashUserNameTupleList) == 0):
        break
    word = word.lower()
    bytepass = word.encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this pass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            passwordFile.write(str(hashedPass).upper() + ":" + str(word).strip() + "\n" )
            hashUserNameTupleList.pop(shadowCount)
        shadowCount += 1
endTime = time.time()
print("Finished cracking dictionary passwords in %.2f seconds." % (endTime-startTime))
#
#Tell how many passwords we not cracked and which usersnames they belonged to
print(str(len(hashUserNameTupleList)),"passwords were not cracked, the uncracked user(s) are:")
for hashUserNameTuple in hashUserNameTupleList:
    print("\t" + hashUserNameTuple[1])
