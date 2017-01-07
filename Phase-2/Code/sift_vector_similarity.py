import os.path
import re
from scipy import spatial


def getTokens(l):
    tokens = filter(None, re.split('<|>|;|\[|\]|,|\n|\s', l))
    return tokens[0:1] + map(float, tokens[1:len(tokens)])


def addCellsInFrame(frame, res):
    for i in xrange(res*res):
        frame.append(list())


def addFrameInSiftData(siftData, currentFrameNum, previousFrameNum, res):
    while (currentFrameNum > previousFrameNum):
        siftData.append(list())  # add new frame in list
        addCellsInFrame(siftData[len(siftData) - 1], res)  # add empty cells in frame
        previousFrameNum +=1


def siftVectorOfVideo(siftFile, res):
    lastVideoNum = None
    siftVector = list()
    lastLineNum = None
    l = siftFile.readline()
    if len(l)==0:
        print 'Data for the video could not be found in the input file...\n'
        return siftVector

    lineData = getTokens(l)
    videoNum = lastVideoNum = lineData[0]
    currentFrameNum = lineData[1]
    previousFrameNum = 0
    addFrameInSiftData(siftVector, currentFrameNum, previousFrameNum,res)
    siftVector[int(lineData[1] - 1)][int(lineData[2] - 1)].append(lineData[7:len(lineData)])
    previousFrameNum = currentFrameNum
    count=1
    while videoNum == lastVideoNum: #and count < 10:
        lastVideoNum = videoNum
        lastLine = siftFile.tell()
        l = siftFile.readline()
        if len(l)>0:
            lineData = getTokens(l)
            videoNum = lineData[0]
            currentFrameNum = lineData[1]
            if(lastVideoNum==videoNum):
                if currentFrameNum > previousFrameNum:
                    addFrameInSiftData(siftVector, currentFrameNum, previousFrameNum, res)
                siftVector[int(lineData[1]-1)][int(lineData[2]-1)].append(lineData[7:len(lineData)])
                previousFrameNum = currentFrameNum
        else:
            break
        count+=1

    siftFile.seek(lastLine, 0)
    #print count
    return siftVector


def getSimilarityNew(c1,c2, simMeasure):
    if simMeasure == 1:
        similarityFunction = spatial.distance.cosine
    else:
        similarityFunction = spatial.distance.euclidean

    similarDescriptors = 0
    for i in c1:
        dis = list()
        for j in c2:
            dis.append(similarityFunction(i, j))
        dis.sort()

        if dis[1]>=1.5*dis[0]:
            similarDescriptors+=1

    similarity = float(similarDescriptors)/len(c1)

    return similarity


def seekToVideo(file, v1, v2):
    readName = None
    lastLine = file.tell()
    while True:
        l = file.readline()
        endOfName = 1
        while l[endOfName]!=';':
            endOfName+=1
        readName = l[1:endOfName]
        if readName == v1 or readName == v2:
            break
        lastLine = file.tell()

    file.seek(lastLine)
    return (readName,lastLine)


def compare(h1, h2, res, simMeasure, isRangeSearch):
    # Main function to compute similarity of two video's sift vectors.
    a = h1 if len(h1) >= len(h2) else h2
    b = h1 if len(h1) < len(h2) else h2
    noOfShifts = len(a) - len(b) + 1
    maxSim = -1
    noOfCells = res * res
    totalFrames = 1

    if isRangeSearch and len(b) > 0:
        totalFrames = len(b)
    elif len(a) > 0:
        totalFrames = len(a)

    for i in xrange(noOfShifts):
        similarityOfSequence = 0
        for j in xrange(len(b)):
            similarityOfFrame = 0
            for k in xrange(noOfCells):
                if j+i < len(a) and k < len(b[j]):
                    similarityOfCell = (getSimilarityNew(b[j ][ k], a[j + i][ k], simMeasure))
                    similarityOfFrame += similarityOfCell
            similarityOfSequence += similarityOfFrame / noOfCells

        if similarityOfSequence/totalFrames > maxSim:
            maxSim = similarityOfSequence/ totalFrames

    return maxSim


def computeSimilarityCosineSift(v1, v2, filename, res, v1Range, v2Range):
    return computeSimilarity(v1, v2, filename, res, 1, v1Range, v2Range)


def computeSimilarityL2Sift(v1, v2, filename, res, v1Range, v2Range):
    return computeSimilarity(v1, v2, filename, res, 2, v1Range, v2Range)


def computeSimilarity(v1,v2,filename,res,simMeasure,v1Range, v2Range, isRangeSearch=True):

    if os.path.isfile(filename):
        siftVectorFile = open(filename, 'U')
        videoFound = seekToVideo(siftVectorFile,v1,v2)
        videoFound2 = ('', None)

        if len(videoFound[0]) == 0:
            print 'Video not found in the input file'
            return -1

        video1Sift = siftVectorOfVideo(siftVectorFile, res)
        if v1 == v2:
            siftVectorFile.seek(videoFound[1])
            videoFound2 = (v1, videoFound[1])
        elif videoFound[0] == v1:
            videoFound2 = seekToVideo(siftVectorFile, v2, v2)
        else:
            videoFound2 = seekToVideo(siftVectorFile, v1, v1)

        if len(videoFound2[0])==0:
            print 'Video not found in the input file'
            return -1

        video2Sift = siftVectorOfVideo(siftVectorFile, res)

        if videoFound[0] == v2:
            tempList = video1Sift
            video1Sift = video2Sift
            video2Sift = tempList

        if v1Range[1] < len(video1Sift):
            startRangeV1 = (v1Range[0] if v1Range[0]>=0 else 0)
            endRangeV1 = (v1Range[1])+1
        if v2Range[1] < len(video2Sift):
            startRangeV2 = (v2Range[0] if v2Range[0] >= 0 else 0)
            endRangeV2 = (v2Range[1]) + 1

        startRangeV1 = startRangeV2 = 0
        endRangeV1 = endRangeV2 = 1000

        video1Sift = video1Sift[startRangeV1:endRangeV1]
        video2Sift = video2Sift[startRangeV2:endRangeV2]

        return compare(video1Sift, video2Sift, res, simMeasure, isRangeSearch)

    else:
        print 'Filename incorrect!'
