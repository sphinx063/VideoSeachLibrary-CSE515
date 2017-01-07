import re
import numpy
from sklearn.decomposition import PCA

def principal_component_analysis(fileName, dimensions):
    f = open(fileName, 'r')
    fw = open(fileName + '.pca.' + str(dimensions), 'w')
    fwe = open(fileName + '.pca.eigen.' + str(dimensions), 'w')

    data = []
    video_info = []
    while 1:
        features = split_line_into_tokens(f.readline())
        if not features:
            break
        data.append(features[3:])
        video_info.append(features[:5])
    pca = PCA(dimensions)
    transformedData = pca.fit_transform(data).tolist()
    index = 0
    for row in transformedData:
        finalfeatures = video_info[index] + row
        fw.write("; ".join(map(lambda x: str(x), finalfeatures)) + "\n")
        index = index + 1
    fw.close()
    eigValues, eigVectors = numpy.linalg.eig(numpy.cov(numpy.array(data).astype(float).transpose()))
    index = 1
    for entry in eigVectors.transpose().tolist():
        d = []
        v = []
        innerIndex = 1
        for value in entry:
            d.append(innerIndex)
            v.append(value)
            innerIndex = innerIndex + 1
        s = sorted(v, reverse=True)
        sl = []
        for val in s:
            tup = (d[v.index(val)], val)
            sl.append(tup)
        fwe.write("Dimension" + str(index) + " = [" + " , ".join(map(lambda x: str(x), sl)) + "]" + "\n")
        if index == dimensions:
            break
        index = index + 1
    fwe.close()


def split_line_into_tokens(line):
    line = line.replace("<", "")
    line = line.replace(">", "")
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.strip('\r\n')
    tokens = re.split(';|,| ', line)
    tokens = filter(None, tokens)
    return tokens


principal_component_analysis("/Users/sruthimaddineni/Desktop/phase3_input.sift", 10)
#principal_component_analysis("/Users/sruthimaddineni/Desktop/Fall'16/MWDB/Project/Phase 1/Results/DataR.chst", 6)