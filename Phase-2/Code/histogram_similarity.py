import os.path
import re
from scipy import spatial


def getTokens(l):
    tokens = filter(None, re.split('<|>|;|\[|\]|,|\n|\s', l))
    return tokens[0:1]+map(float,tokens[1:len(tokens)])


def histogramOfVideo(histFile):
    lastVideoNum=None
    histogram = list()
    lastLineNum = None
    l = histFile.readline()
    if len(l)==0:
        return
    lineData = getTokens(l)
    videoNum = lastVideoNum = lineData[0]

    while videoNum == lastVideoNum:
        histogram.append(lineData[3:len(lineData)])
        lastVideoNum = videoNum
        lastLine = histFile.tell()
        l = histFile.readline()
        if len(l)==0:
            break
        lineData = getTokens(l)
        videoNum = lineData[0]

    histFile.seek(lastLine,0)

    return histogram


def compare(h1,h2, res, simMeasure, isRangeSearch):
    #Assuming h2 is smaller in length than h1
    a = h1 if len(h1) >= len(h2) else h2
    b = h1 if len(h1) < len(h2) else h2
    if simMeasure == 1:
        similarityFunction = normalisedL1metric
    else:
        similarityFunction = intersectionSimilarity
    noOfShifts = len(a) - len(b) + 1
    maxSim = -1
    noOfCells = res*res
    for i in xrange(0,noOfShifts, noOfCells):
        similarityOfSequence = 0
        for j in xrange(0, len(b), noOfCells):
            similarityOfFrame = 0
            print "Comparing Frames " + str(j) + "  " + str(j+i)
            for k in xrange(noOfCells):
                if j+k>len(b) or j+i+k > len(a):
                    print 'Data not found according to the resolution specified...Exiting and returning partial smialrity'
                    break
                similarityOfFrame += (similarityFunction(b[j + k], a[j + i + k]))
            similarityOfSequence += similarityOfFrame/noOfCells
        totalFrames = 1
        print len(a), len(b)
        if isRangeSearch and len(b)>0:
            totalFrames = len(b)/noOfCells
        elif len(a)>0:
            totalFrames = len(a) / noOfCells
        if similarityOfSequence/totalFrames > maxSim:
            maxSim = similarityOfSequence/ totalFrames
    return maxSim


def normalisedL1metric(a,b):
    num = 0
    den = 0
    for i in xrange(min(len(a), len(b))):
        num += spatial.distance.cityblock(a[i],b[i])
        den += max(a[i], b[i])
    if den != 0:
        return 1 - (num / den)
    else:
        return 1 - 0


def intersectionSimilarity(a, b):
    num = 0
    den = 0
    for i in xrange(min(len(a),len(b))):
        num += min(a[i],b[i])
        den += max(a[i],b[i])
    if den!=0:
        return (num/den)
    else:
        return 0



def seekToVideo(file, v1, v2):
    readName = None
    lastLine = file.tell()
    l = 'initialTempValue'
    while True and len(l)>0:
        l = file.readline()
        if len(l)>0:
            endOfName = 1
            while l[endOfName]!=';':
                endOfName+=1
            readName = l[1:endOfName]
            if readName == v1 or readName == v2:
                break
            lastLine = file.tell()

    file.seek(lastLine)
    return (readName,lastLine)


def computeSimilarityL1Hist(v1, v2, filename, res, v1Range, v2Range):
    print v1, v2, filename, res, v1Range, v2Range
    return computeSimilarity(v1, v2, filename, res, 1, v1Range, v2Range)


def computeSimilarityIntersectionHist(v1, v2, filename, res, v1Range, v2Range):
    return computeSimilarity(v1, v2, filename, res, 2, v1Range, v2Range)


def computeSimilarity(v1,v2,filename,res,simMeasure,v1Range, v2Range, isRangeSearch=True):
    if os.path.isfile(filename):
        histFile = open(filename, 'U')
        videoFound = seekToVideo(histFile,v1,v2)
        videoFound2 = ('',None)
        if len(videoFound[0])==0:
            print 'Video not found in the input file'
            return -1
        video1Hist = histogramOfVideo(histFile)

        if v1 == v2:
            histFile.seek(videoFound[1])
            videoFound2 = (v1,videoFound[1])
        elif videoFound[0] == v1:
            videoFound2 = seekToVideo(histFile, v2, v2)
        else:
            videoFound2 = seekToVideo(histFile, v1, v1)
        if len(videoFound2[0])==0:
            print 'Video not found in the input file'
            return -1

        video2Hist = histogramOfVideo(histFile)

        if videoFound[0] == v2:
            tempList = video1Hist
            video1Hist = video2Hist
            video2Hist = tempList

        startRangeV1 = startRangeV2 = 0
        endRangeV1 = endRangeV2 = 1000

        if v1Range[1] < len(video1Hist):
            startRangeV1 = res*res*(v1Range[0] if v1Range[0]>=0 else 0)
            endRangeV1 = (v1Range[1]*res*res)+1*res*res
        if v2Range[1] < len(video2Hist):
            startRangeV2 = res * res * (v2Range[0] if v2Range[0] >= 0 else 0)
            endRangeV2 = (v2Range[1] * res * res) + 1 * res * res

        video1Hist = video1Hist[startRangeV1:endRangeV1]
        video2Hist = video2Hist[startRangeV2:endRangeV2]

        similarity = compare(video1Hist, video2Hist, res, simMeasure, isRangeSearch)

        #print 'Similarity - ', compare(video1Hist, video2Hist, res, simMeasure, False)
        return similarity
    else:
        print 'Filename incorrect!'
        return -1