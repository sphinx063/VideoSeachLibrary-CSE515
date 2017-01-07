from operator import itemgetter
import imageio
import os

import sift_vector_similarity as siftsim

rootDir = './P3DemoVideos'
sift_file = 'phase3_input.sift.pca.10'
videoNames = []
r = 2
dict1 = {}
k = 2
k_1 = 10
output_file1 = open('phase3_input_10_2.gspc', 'w')
output_file2 = open('phase3_input_10_10.gspc', 'w')
similarities = {}

skip_videos = {}

def get_video_names():
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.endswith('.mp4'):
               videoNames.append(os.path.join(rootDir, fname))
    #print videoNames
    
def compute_graph():
    for video in videoNames:
        vid = imageio.get_reader(video, 'ffmpeg')
        num_frames = vid._meta['nframes'] - 1
        tokens = video.split('/')
        video_name = tokens[len(tokens) - 1].strip()
        if video_name in skip_videos:
           continue
        for frame in range(1, num_frames + 1):
             get_top_k_frames(video_name, frame, k)
    output_file1.close()
    output_file2.close()
    
def get_top_k_frames(v1, f1, k):
    result = {}
    for video_name in videoNames:
        vid = imageio.get_reader(video_name, 'ffmpeg')
        num_frames = vid._meta['nframes'] - 1
        tokens = video_name.split('/')
        v2 = tokens[len(tokens) - 1].strip()
        for f2 in range(1, num_frames + 1):
            if (v1 != v2) and (f1 != -7):
               vector_1 = dict1[v1 + ',' + str(f1)]
               vector_2 = dict1[v2 + ',' + str(f2)]
               #print "Similarity Calculation"
               key = v1 + ',' + str(f1) + ',' + v2 + ',' + str(f2)
               key_reverse = v2+ ',' + str(f2) + ',' + v1 + ',' + str(f1)
               if similarities.get(key) != None:
                   result[key] = similarities[key]
               elif similarities.get(key_reverse) != None:
                   result[key] = similarities[key_reverse]
               else:
                   sim = siftsim.computeFrameSimilarityEuclidean(vector_1, vector_2)
                   result[key] = sim;
                   similarities[key] = sim;
                   #print "Similarity computed for " + key
    result = sorted(result.items(), key=itemgetter(1), reverse=True)
    for row in result[:k]:
        tokens = row[0].split(',')
        output_file1.write('{<'+tokens[0]+','+tokens[1]+'>,<'+tokens[2]+','+tokens[3]+'>,'+str(row[1])+'}\n')
    for row in result[:k_1]:
        tokens = row[0].split(',')
        output_file2.write('{<'+tokens[0]+','+tokens[1]+'>,<'+tokens[2]+','+tokens[3]+'>,'+str(row[1])+'}\n')

def get_sift_vectors(inputFile):
    input_file = open(inputFile, 'r').readlines()
    for line in input_file:
        values = line.replace('<', '').replace('>', '').strip().split(';')
        key = values[0].strip() + ',' + values[1].strip()
        cell_num = int(values[2].strip())
        vector = values[3:]
        desc_vector = [float(x.strip()) for x in vector]
        if (dict1.get(key) == None):
            dict1[key] = [[] for i in range(r*r)]
        dict1[key][cell_num-1].append(desc_vector)

get_sift_vectors(sift_file)
get_video_names()
compute_graph()
