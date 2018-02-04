def main():
    planetsFile = open("planetnames.txt","r")
    outfile = open("planetwordlist.txt","w")
    planetsList = list()
    doublePlanetsList = list()
    triplePlanetsList = list()
    planetsSubstutionList = list()
    doublePlanetsSubstutionList = list()
    triplePlanetsSubstutionList = list()
    masterSubstutionList = list()
    count = 0
    for planetName in planetsFile:
        planetsList.append(planetName)
    for planetName in planetsList:
        for secondPlanetName in planetsList:
            doublePlanetsList.append("" + planetName.strip() + secondPlanetName)
            for thridPlanetName in planetsList:
                triplePlanetsList.append("" + planetName.strip() + secondPlanetName.strip() + thridPlanetName)


    for planetName in planetsList:
        outfile.write(planetName)
        masterSubstutionList.append(planetName)
    outfile.flush()
    for doublePlanetName in doublePlanetsList:
        outfile.write(doublePlanetName)
        masterSubstutionList.append(doublePlanetName)
    outfile.flush()
    # for triplePlanetName in triplePlanetsList:
    #     outfile.write(triplePlanetName)
    #     masterSubstutionList.append(triplePlanetName)
    # print(len(masterSubstutionList))
    for password in masterSubstutionList:
        index = 0
        for char in password:
            if(char == 'o' or char == 'e' or char == 's'):
                masterSubstutionList.append(substituteIndex(password,index))
            index += 1
    print(len(masterSubstutionList))
    for subName in masterSubstutionList:
        outfile.write(subName)


    planetsFile.close()
    outfile.close()
def countSubstitutions(password):
    substitutionCount = 0
    for char in password:
        if(char == 'o' or char == 'e' or char == 's'):
            substitutionCount += 1
    return substitutionCount
def substituteIndex(stringToSub, index):
    if(stringToSub[index] == 'o'):
        stringToSub = stringToSub[0:index] + '0'+ stringToSub[index+1:len(stringToSub)]
    elif(stringToSub[index] == 'e'):
        stringToSub = stringToSub[0:index] + '3'+ stringToSub[index+1:len(stringToSub)]
    elif(stringToSub[index] == 's'):
        stringToSub = stringToSub[0:index] + '5'+ stringToSub[index+1:len(stringToSub)]
    return stringToSub


def substituteIndexTest():
    hello = "moocowmoo"
    print(countSubstitutions(hello))
    for i in range(len(hello)):
        hello = substituteIndex(hello,i)
        print(hello)
main()
