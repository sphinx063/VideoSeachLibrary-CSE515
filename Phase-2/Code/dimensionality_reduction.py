import re
import numpy
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def principal_component_analysis(fileName, dimensions):
    f = open(fileName, 'r')
    fw = open(fileName + '.pca', 'w')
    data = []
    video_info = []
    while 1:
        features = split_line_into_tokens(f.readline())
        if not features:
            break
        data.append(features[3:])
        video_info.append(features[:3])
    pca = PCA(dimensions)
    transformedData = pca.fit_transform(data).tolist()
    index = 0
    for row in transformedData:
        finalfeatures = video_info[index] + row
        fw.write("; ".join(map(lambda x: str(x), finalfeatures)) + "\n")
        index = index + 1
    eigValues, eigVectors = numpy.linalg.eig(numpy.cov(numpy.array(data).astype(float).transpose()))
    print "Eigen values are [" + " , ".join(map(lambda x: str(x), eigValues)) + "]"
    index = 1
    for entry in eigVectors.transpose().tolist():
        print "Dimension" + str(index) + " = [" + " , ".join(map(lambda x: str(x), entry)) + "]"
        index = index + 1


def k_means(fileName, dimensions):
    f = open(fileName, 'r')
    fw = open(fileName + '.km', 'w')
    data = []
    video_info = []
    while 1:
        features = split_line_into_tokens(f.readline())
        if not features:
            break
        data.append(features[3:])
        video_info.append(features[:3])
    kmeans = KMeans(dimensions)
    transformedData = kmeans.fit_transform(data).tolist()
    index = 0
    for row in transformedData:
        finalfeatures = video_info[index] + row
        fw.write("; ".join(map(lambda x: str(x), finalfeatures)) + "\n")
        index = index + 1


def split_line_into_tokens(line):
    line = line.replace("<", "")
    line = line.replace(">", "")
    line = line.replace("[", "")
    line = line.replace("]", "")
    line = line.strip('\r\n')
    tokens = re.split(';|,| ', line)
    tokens = filter(None, tokens)
    return tokens