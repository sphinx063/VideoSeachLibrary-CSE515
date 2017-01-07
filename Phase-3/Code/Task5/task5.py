import timeit

import gc

from nearpymod import Engine
from nearpymod.hashes import RandomBinaryProjections

import os.path
import re


#Function to remove all the whitespaces and special characters from the
# read line for processing just numbers according to their position
def getTokens(l):
    tokens = filter(None, re.split('<|>|;|\[|\]|,|\n|\s', l))
    return tokens[0:1] + map(float, tokens[1:len(tokens)])


#Storing vectors in the nearpy engine after reading them from the file
def storeVectors(inFile, engine, outFile):
    lineCount = 0
    lines = ''
    while(True):
        l = inFile.readline()

        if len(l)<1:
            break

        linedata = getTokens(l)
        vectorStoreList = engine.store_vector(linedata[3:5])

        layer=0
        output=''
        for keyList in vectorStoreList:
            output += '{'
            output+=str(layer) + ',' + str(keyList[0])+',<'
            output+= (linedata[0]+';'+str(int(linedata[1]))+';'+str(int(linedata[2]))+';'+str(linedata[3])+';'+str(linedata[4]))
            output+='>}'
            output+='\n'
            layer+=1

        lines+=output
        lineCount += 1
        if lineCount>10000:
            lineCount=0
            outFile.write(lines)
            lines=''
            gc.collect()
    outFile.write(lines)


#Function to create an LSH file
def createLSHFile(inputFilename, L, K):
    if os.path.isfile(inputFilename):
        siftVectorFile = open(inputFilename, 'r')
        # Dimension of our vector space
        dimension = 2
        noOfLayers = L
        noOfBits = K
        layers = []
        for i in xrange(noOfLayers):
            # Create a random binary hash with 10 bits
            layers.append(RandomBinaryProjections('layer' + str(i), noOfBits))

        # Create engine with pipeline configuration
        engine = Engine(dimension, lshashes=layers)
        outFile = open('filename_d.lsh','w')
        storeVectors(siftVectorFile, engine, outFile)
        outFile.close()
        siftVectorFile.close()

    else:
        print 'Filename incorrect!'


#Main function for taking input on prompt
def main():

    #Uncomment the following for taking input by prompt.
    ''''''
    inputFilename = raw_input('Enter the input filename: ')
    L = int(raw_input('Enter L: '))
    K = int(raw_input('Enter K: '))
    ''''''

    '''
    inputFilename = 'phase3_input.sift.pca.10'
    L = 6
    K = 10
    '''
    start_time = timeit.default_timer()
    createLSHFile(inputFilename, L, K)
    elapsed = timeit.default_timer() - start_time
    print 'Finished in - ', elapsed, 'seconds'


main()

''''
def test():
    # Dimension of our vector space
    dimension = 2
    noOfLayers = 4
    layers=[]
    for i in xrange(noOfLayers):
        # Create a random binary hash with 10 bits
        layers.append(RandomBinaryProjections('layer'+str(i), 10))

    # Create engine with pipeline configuration
    engine = Engine(dimension, lshashes=layers)

    # Index 1000000 random vectors (set their data to a unique string)
    noOfVectors = 2
    v = []
    vectorStoreList=[]
    for index in range(noOfVectors):
        v.append(numpy.random.randn(dimension))
        vectorStoreList.append(engine.store_vector(v[index], 'data_%d' % index))
    print v, vectorStoreList

    vectorKeyMap = []

    for i in xrange(noOfLayers):
        vectorKeyMap.append({})

    for j in xrange(noOfLayers):
        for i in engine.storage.get_all_bucket_keys('layer'+str(j)):
            print i, engine.storage.get_bucket('layer'+str(j), i)

    for j in xrange(noOfLayers):
        for i in engine.storage.get_all_bucket_keys('layer' + str(j)):
            for data in engine.storage.get_bucket('layer' + str(j), i):
                vectorKeyMap[j][data[1]] = i

    for i in xrange(noOfLayers):
        print i
        for j in range(noOfVectors):
            dataStr = 'data_%d' % j
            print i, dataStr, vectorKeyMap[i][dataStr]

    # Create random query vector
    query = numpy.random.randn(dimension)

    # Get nearest neighbours
    N = engine.neighbours(query)

    print N
'''
