import sys

def splitScore(simpleScore):
    simpleScore = simpleScore.strip()
    scoreList = simpleScore.split(' ')
    return scoreList

def isValidBase(baseChar):
    if type(baseChar) != type(""):
        print "Type of base should be string"
        return False
    if len(baseChar) > 1:
        print "Base should be one char string"
        return False
    if not (baseChar in ('C' ,'D', 'E', 'F', 'G', 'A', 'B')):
        print "Base should only be one of C D E F G A B"
        return False
    return True

def isValidNote(note):
    curNote = note.strip()
    if curNote == '':
        print "Input note should not just contain space or empty"
        return False
    numCharOfNote = curNote[0]
    if not (numCharOfNote.isdigit() and 1 <= int(numCharOfNote) and \
            int(numCharOfNote) <= 7):
        print "The first char of input note", note, "should be digit within range 1~7"
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

def getTranslateTable():
    curNote = 0
    translateTable = []
    timeOf2_3Exchange = 0
    while curNote <= 128:
        timeOf2_3Exchange = timeOf2_3Exchange + 1
        translateTable.append(curNote)
        if timeOf2_3Exchange % 2 == 1:
            for i in xrange(2):
                curNote = curNote + 2
                translateTable.append(curNote)
        else:
            for i in xrange(3):
                curNote = curNote + 2
                translateTable.append(curNote)
        curNote = curNote + 1
    return translateTable

def valueInTranslateTable(baseChar):
    baseCharIndexInTable = {
        "C": 60,
        "D": 62,
        "E": 64,
        "F": 65,
        "G": 67,
        "A": 69,
        "B": 71,
    }
    return baseCharIndexInTable[baseChar]

def translate(note, baseChar, translateTable):
    curNote = note.strip()
    numOfNote = int(curNote[0])
    signOfNote = curNote[1:]

    distanceOfNoteAndBase = numOfNote - 1
    baseValueInTranslateTable = valueInTranslateTable(baseChar)
    baseIndexInTranslateTable = translateTable.index(baseValueInTranslateTable)
    offsetBySign = len(signOfNote) * 7
    if offsetBySign > 0 and signOfNote[0] == 'd':
        offsetBySign = -1 * offsetBySign
    return translateTable[distanceOfNoteAndBase + baseIndexInTranslateTable \
            + offsetBySign]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        baseChar = sys.argv[1]
        if not isValidBase(baseChar):
            print "Base should only be one char within set {C,D,E,F,G,A,B}"
            sys.exit(1)

        simpleScore = sys.argv[2]
        noteListOfSimpleScore = splitScore(simpleScore)
        for note in noteListOfSimpleScore:
            if isValidNote(note):
                print translate(note, baseChar, getTranslateTable()),
            else:
                print "Input ", note," is invalid"
                print "Input note should range between 1~7 with several u or d fellowing"
                print "u means up, d means down, only one of them should occur each time"
                sys.exit(1)
    else:
        print "Invalid arguments"
        print "Usage: python music.x.py $1=C, $2(simple score)"

