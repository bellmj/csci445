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
for line in shadowFile:#add usersnames and hashes to hashUserNameTupleList
    lineList = line.split(':')
    hashUserNameTupleList.append((lineList[1].strip(),lineList[0]))
shadowFile.close()
#open passwordfile and check if we already have any hashes
passwordFile = open("./.sufferWhatTheyMust",'r')

for line in passwordFile:##todo fix this garbage
    print(line)
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:
        print("help ",hashUserNameTuple[0],line.split(':')[0])
        if(hashUserNameTuple[0] == line.split(':')[0]):
            hashUserNameTupleList.pop(shadowCount)
            shadowCount -= 1
    shadowCount += 1
passwordFile.close()
passwordFile = open("./.sufferWhatTheyMust",'a')
#Start numbercracking
numpass = 0
startTime = time.time()
while numpass <= 9999 and len(hashUserNameTupleList) != 0:#four digit
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
    bytepass = str(numpass).zfill(5).encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this numpass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            hashUserNameTupleList.pop(shadowCount)
            # print(len(hashUserNameTupleList),"passwords left to crack")
        shadowCount += 1
    numpass += 1
numpass = 0
while numpass <= 999999 and len(hashUserNameTupleList) != 0:#six digit
    bytepass = str(numpass).zfill(6).encode('utf-8')
    m = hashlib.md5()
    m.update(bytepass)
    hashedPass = m.hexdigest()
    shadowCount = 0
    for hashUserNameTuple in hashUserNameTupleList:#check each guess across all passhashes given
        if(hashedPass.lower() == hashUserNameTuple[0].lower()):#if this numpass is a collison with user pass
            print("\t" + str(hashUserNameTuple[1]) + ":" + str(bytepass).split('\'')[1])
            hashUserNameTupleList.pop(shadowCount)
            # print(len(hashUserNameTupleList),"passwords left to crack")
        shadowCount += 1
    numpass += 1
endTime = time.time()
print("Finished cracking numerical passwords in %.2f seconds." % (endTime-startTime))

print("Starting dictionary crack")
dictionaryFile = open("/usr/share/dict/words",'r')
fourChacDictList = list()
fiveCharDictList = list()
dictList = list()
startTime = time.time()
for word in dictionaryFile:
    word = word.strip()
    # if(len(word) == 4):


#
#Tell how many passwords we not cracked and which usersnames they belonged to
print(str(len(hashUserNameTupleList)),"passwords were not cracked, the uncracked users are:")
for hashUserNameTuple in hashUserNameTupleList:
    print("\t" + hashUserNameTuple[1])
