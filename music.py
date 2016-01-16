import sys

def isValid(inputStr):
    for item in inputStr:
        if not item.isdigit():
            return False
    return True

def initTable(base):
    bucket = list()
    time = 0
    curNum = 0
    while curNum <= 128:
        time = time + 1
        bucket.append(curNum)
        if time % 2 == 1:
            for i in xrange(2):
                curNum = curNum + 2
                bucket.append(curNum)
        else:
            for i in xrange(3):
                curNum = curNum + 2
                bucket.append(curNum)
        curNum = curNum + 1

    table = dict()
    indexOfMiddleC = bucket.index(60)
    indexOfMiddleA = bucket.index(69)
    if base < 3:
        indexOfBase = indexOfMiddleA + base - 1
    else:
        indexOfBase = indexOfMiddleC + base - 3

    loopOf7 = 0
    cur = indexOfBase
    while cur < len(bucket) and bucket[cur] <= 128:
        for i in xrange(7):
            tmpStr = "u" * loopOf7
            tmpStr = str(i + 1) + tmpStr
            table[tmpStr] = bucket[cur]
            cur = cur + 1
        loopOf7 = loopOf7 + 1

    loopOf7 = 1
    cur = indexOfBase - 1
    while cur >=0 and bucket[cur] >= 0:
        for i in xrange(7, 0, -1):
            tmpStr = "d" * loopOf7
            tmpStr = str(i) + tmpStr
            table[tmpStr] = bucket[cur]
            cur = cur - 1
        loopOf7 = loopOf7 + 1
                
    return table

def process(inputStr, base):
    table = initTable(base)
    return map(lambda x: table[x], inputStr)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        if not sys.argv[1].isdigit():
            print "default base code is invalid"
            print "valid code is between A and G, which represents a number between 1 and 7"
            sys.exit(1)

        base = int(sys.argv[1])
        if not (base <= 7 and base >= 1):
            print "invalid base, the correct base must be set between 1 and 7"
            sys.exit(1)

        inputStr = sys.argv[2]
        inputStr = inputStr.strip()
        inputStr = inputStr.split(' ')
        
        if not isValid(inputStr):
            print "input string is invalid"
            print "valid form: xx xx xx xx xx"
            sys.exit(1)

        postProcessStr = process(inputStr, base)

        for i in xrange(len(postProcessStr) - 1):
            print postProcessStr[i],
        print postProcessStr[-1]
        sys.exit(0)

    else:
        print "invalid arguments number"
        print "Usage: $1(means $1=1, in which 1:A - 7:G), $2(inputStr)"
        sys.exit(1)
