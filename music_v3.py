
def splitScore(simpleScore):
    simpleScore = simpleScore.strip()
    scoreList = [note for note in simpleScore.split(' ') if note != '']
    return scoreList

def isValidBase(baseChar):
    if type(baseChar) != type(""):
        print "Type of base should be string"
        return False
    if len(baseChar) > 2:
        print "Base should be a string with its length <= 2"
        return False
    if baseChar[0] not in ('C' ,'D', 'E', 'F', 'G', 'A', 'B'):
        print "Base should only be one of C D E F G A B"
        return False
    if len(baseChar) == 2 and baseChar[1] not in ('u', 'd'):
        print "Base should only be one of C D E F G A B with a single char appendix of 'u' or 'd'"
        return False
    return True

def isValidScale(scale):
    if scale in ("ma", "Ma", "mA", "MA",
            "nm", "Nm", "nM", "NM",
            "hm", "Hm", "hM", "HM",
            "mm", "Mm", "mM", "MM"):
        return True
    return False
    

def isValidNote(note):
    curNote = note.strip()
    if curNote == '':
        print "Input note should not just contain space or empty"
        return False
    numCharOfNote = curNote[0]
    if not (numCharOfNote.isdigit() and 0 <= int(numCharOfNote) and \
            int(numCharOfNote) <= 7):
        print "The first char of input note", note, "should be digit within range 0~7"
        return False
    signOfNote = curNote[1:]
    if len(signOfNote) > 0:
        firstSign = signOfNote[0]
        if firstSign != "d" and firstSign != "u":
            print "The sign of input note should only be 'u' or 'd'"
            return False
        for eachSign in signOfNote[1:]:
            if eachSign != firstSign:
                print "There should be only 'u's or 'd's in the string of sign"
                return False

    return True

def valueOfBase(baseChar):
    baseCharValueDict = {
        "C": 60,
        "Cu": 61,
        "Dd": 61,
        "D": 62,
        "Du": 63,
        "Ed": 63,
        "E": 64,
        "F": 65,
        "Fu": 66,
        "Gd": 66,
        "G": 67,
        "Gu": 68,
        "Ad": 68,
        "A": 69,
        "Au": 70,
        "Bd": 70,
        "B": 71,
    }
    return baseCharValueDict[baseChar]

def getDictOfHalfStepFromBase(scale):
    dictOfHalfStepFromBase = dict()
    if scale == "ma":
        dictOfHalfStepFromBase[1] = 0
        dictOfHalfStepFromBase[2] = 2
        dictOfHalfStepFromBase[3] = 4
        dictOfHalfStepFromBase[4] = 5
        dictOfHalfStepFromBase[5] = 7
        dictOfHalfStepFromBase[6] = 9
        dictOfHalfStepFromBase[7] = 11
    else:
        dictOfHalfStepFromBase[1] = 0
        dictOfHalfStepFromBase[2] = 2
        dictOfHalfStepFromBase[3] = 3
        dictOfHalfStepFromBase[4] = 5
        dictOfHalfStepFromBase[5] = 7
        dictOfHalfStepFromBase[6] = 8
        dictOfHalfStepFromBase[7] = 10
        if scale == "hm":
            dictOfHalfStepFromBase[7] = 11
        elif scale == "mm":
            dictOfHalfStepFromBase[6] = 9
            dictOfHalfStepFromBase[7] = 11
    return dictOfHalfStepFromBase

def translate(note, baseChar, dictOfHalfStepFromBase):
    curNote = note.strip()
    numOfNote = int(curNote[0])
    signOfNote = curNote[1:]
    
    if numOfNote == 0:
        return 0

    halfStepsFromBase = dictOfHalfStepFromBase[numOfNote]
    baseValue = valueOfBase(baseChar)
    offsetBySign = len(signOfNote) * 12
    if offsetBySign > 0 and signOfNote[0] == 'd':
        offsetBySign = -1 * offsetBySign
    return halfStepsFromBase + baseValue + offsetBySign

def mergeSimilarRow(measureLineList):
    rowGroupList = list()
    for measureLine in measureLineList:
        if len(rowGroupList) == 0:
            group = list()
            group.append(measureLine)
            rowGroupList.append(group)
        else:
            if len(rowGroupList[-1][0]) != len(measureLine):
                group = list()
                group.append(measureLine)
                rowGroupList.append(group)
            else:
                rowGroupList[-1].append(measureLine)
    return rowGroupList


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        baseChar = sys.argv[1]
        if not isValidBase(baseChar):
            print "Base should only be one char within set {C,D,E,F,G,A,B}, a single sign of u or d is permitted"
            sys.exit(1)

        scale = sys.argv[2]
        if not isValidScale(scale):
            print \
"""
Scale should only be major, Nminor, Hminor, Mminor
You should use notation for each scale:
    "ma" : "major",
    "nm" : "Nminor",
    "hm" : "Hminor",
    "mm" : "Mminor" 
"""
            sys.exit(1)

        simpleScoreList = list()
        try:
            with open(sys.argv[3], 'r') as fstream:
                for eachLine in fstream.readlines():
                    simpleScoreList.append(eachLine)
        except IOError:
            inputStringScore = sys.argv[3]
            simpleScoreList = inputStringScore.split('\n')

        dictOfHalfStepFromBase = getDictOfHalfStepFromBase(scale)
        scoreLineList = list()
        for eachScoreLine in simpleScoreList:
            measureList = list()
            if eachScoreLine == '\n':
                continue
            for simpleScore in eachScoreLine.split('|'):
                noteListOfSimpleScore = splitScore(simpleScore)
                noteList = list()
                for note in noteListOfSimpleScore:
                    if isValidNote(note):
                        noteList.append(str(translate(note, baseChar, dictOfHalfStepFromBase)))
                    else:
                        print "Input ", note," is invalid"
                        print "Input note should range between 1~7 with several u or d fellowing"
                        print "u means up, d means down, only one of them should occur each time"
                        sys.exit(1)
                measureList.append(' '.join(noteList))
            scoreLineList.append(measureList)


        from tabulate import tabulate
        for eachGroup in mergeSimilarRow(scoreLineList):
            print tabulate(eachGroup, tablefmt="fancy_grid")
    else:
        print "Invalid arguments"
        print "Usage: python music.x.py $1=C $2(simple score) $3(scale) $4(scoreFile or scoreString)"

