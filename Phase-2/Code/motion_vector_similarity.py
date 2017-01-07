from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import numpy as numpy

v1Range = [-1, -1]
v2Range = [-1, -1]

def computeSimilarityCosineMvect(video1, video2, features_mvect, resolution, src_frame_range, dst_frame_range):
    input_file = open(features_mvect, "r").readlines()
    dict1 = {}
    dict2 = {}
    len1 = 1
    len2 = 1
    num_cells = 1
    for line in input_file:
        line = line.replace("<", "").replace("[", "").replace("]", "").replace(">", "")
        if (line.startswith(video1) or line.startswith(video2)):
            # print line
            values = line.split(";")
            key = values[1].strip() + "," + values[2].strip()
            if (int(values[2].strip()) > num_cells):
                num_cells = int(values[2].strip())
            vector_values = values[3].strip().split(",")
            # print vector_values
            direction = int(vector_values[0].strip())
            x1_value = direction * (int(vector_values[3].strip()))
            x2_value = direction * (int(vector_values[5].strip()))
            y1_value = direction * (int(vector_values[4].strip()))
            y2_value = direction * (int(vector_values[6].strip()))
            if (line.startswith(video1)):
                if (int(values[1].strip()) > len1):
                    len1 = int(values[1].strip())
                if (dict1.get(key) == None):
                    dict1[key] = []
                dict1[key].append(str(x1_value) + " " + str(x2_value) + " " + str(y1_value) + " " + str(y2_value))
            if (line.startswith(video2)):
                if (int(values[1].strip()) > len2):
                    len2 = int(values[1].strip())
                if (dict2.get(key) == None):
                    dict2[key] = []
                dict2[key].append(str(x1_value) + " " + str(x2_value) + " " + str(y1_value) + " " + str(y2_value))

    print "Lengths len1 and len2"
    print len1
    print len2

    if (len1 > len2):
        t = len1
        len1 = len2
        len2 = t
        t_dict = dict1
        dict1 = dict2
        dict2 = t_dict

    if ((v1Range[0] == -1 and v1Range[1] == -1) or (v2Range[0] == -1 and v2Range[1] == -1)):
        print "Inside if "
        diff = len2 - len1
        sim_count = 0
        final_sim = 0.0
        print diff, len1, len2, num_cells
        for d in range(0, diff + 1):
            sim_value_1 = 0
            for i in range(1, len1 + 1):
                for j in range(1, num_cells + 1):
                    print "Comparing frames " + str(i) + " and  " + str(i + d)
                    vectors_1 = dict1.get(str(i) + ',' + str(j), ["0 0 0 0"])
                    vectors_2 = dict2.get(str(i + d) + ',' + str(j), ["0 0 0 0"])
                    len_1 = len(vectors_1)
                    len_2 = len(vectors_2)
                    min_len = min(len_1, len_2)
                    for k in range(0, min_len):
                        vector1 = numpy.array(vectors_1[k].split(" ")).reshape(1, -1)
                        vector2 = numpy.array(vectors_2[k].split(" ")).reshape(1, -1)
                        cosine_sim = (float)(cosine_similarity(vector1, vector2))
                        sim_value_1 = (float)(sim_value_1 + cosine_sim)
                        sim_count = sim_count + 1
        sim_value_1 = (float)(sim_value_1 / sim_count)
        print abs(sim_value_1)
        final_sim = max(final_sim, abs(sim_value_1))
        print "Similarity Value"
        print final_sim
        return final_sim
    else:
        sim_value_1 = 0
        sim_count = 0
        final_sim = 0.0
        frame_range = v1Range[1] - v1Range[0] + 1
        for i in range(0, frame_range):
            for j in range(1, num_cells + 1):
                print "Comparing frames " + str(v1Range[0] + i) + "  " + str(v2Range[0] + i)
                vectors_1 = dict1.get(str(v1Range[0] + i) + ',' + str(j), ["0 0 0 0"])
                vectors_2 = dict2.get(str(v2Range[0] + i) + ',' + str(j), ["0 0 0 0"])
                len_1 = len(vectors_1)
                len_2 = len(vectors_2)
                min_len = min(len_1, len_2)
                for k in range(0, min_len):
                    vector1 = numpy.array(vectors_1[k].split(" ")).reshape(1, -1)
                    vector2 = numpy.array(vectors_2[k].split(" ")).reshape(1, -1)
                    cosine_sim = (float)(cosine_similarity(vector1, vector2))
                    sim_value_1 = (float)(sim_value_1 + cosine_sim)
                    sim_count = sim_count + 1
        sim_value_1 = (float)(sim_value_1 / sim_count)
        print abs(sim_value_1)
        final_sim = max(final_sim, abs(sim_value_1))

        print "Similarity Value"
        print final_sim
        return final_sim


def computeSimilarityL2Mvect(video1, video2, features_mvect, resolution, src_frame_range, dst_frame_range):
    input_file = open(features_mvect, "r").readlines()

    dict1 = {};
    dict2 = {}
    len1 = 1;
    len2 = 1;
    num_cells = 1
    for line in input_file:
        line = line.replace("<", "").replace("[", "").replace("]", "").replace(">", "")
        if (line.startswith(video1) or line.startswith(video2)):
            # print line
            values = line.split(";")
            key = values[1].strip() + "," + values[2].strip()
            if (int(values[2].strip()) > num_cells):
                num_cells = int(values[2].strip())
            vector_values = values[3].strip().split(",")
            # print vector_values
            direction = int(vector_values[0].strip())
            x1_value = direction * (int(vector_values[3].strip()))
            x2_value = direction * (int(vector_values[5].strip()))
            y1_value = direction * (int(vector_values[4].strip()))
            y2_value = direction * (int(vector_values[6].strip()))
            if (line.startswith(video1)):
                if (int(values[1].strip()) > len1):
                    len1 = int(values[1].strip())
                if (dict1.get(key) == None):
                    dict1[key] = []
                dict1[key].append(str(x1_value) + " " + str(x2_value) + " " + str(y1_value) + " " + str(y2_value))
            if (line.startswith(video2)):
                if (int(values[1].strip()) > len2):
                    len2 = int(values[1].strip())
                if (dict2.get(key) == None):
                    dict2[key] = []
                dict2[key].append(str(x1_value) + " " + str(x2_value) + " " + str(y1_value) + " " + str(y2_value))

    print "Lengths len1 and len2"
    print len1
    print len2

    if (len1 > len2):
        t = len1
        len1 = len2
        len2 = t
        t_dict = dict1
        dict1 = dict2
        dict2 = t_dict

    if ((v1Range[0] == -1 and v1Range[1] == -1) or (v2Range[0] == -1 and v2Range[1] == -1)):
        print "Inside if "
        diff = len2 - len1
        sim_count = 0
        final_sim = 0.0
        max_dis = 0.0001
        print diff, len1, len2, num_cells
        for d in range(0, diff + 1):
            sim_value_1 = 0
            for i in range(1, len1 + 1):
                for j in range(1, num_cells + 1):
                    print "Comparing frames " + str(i) + " and  " + str(i + d)
                    vectors_1 = dict1.get(str(i) + ',' + str(j), ["0 0 0 0"])
                    vectors_2 = dict2.get(str(i + d) + ',' + str(j), ["0 0 0 0"])
                    len_1 = len(vectors_1)
                    len_2 = len(vectors_2)
                    min_len = min(len_1, len_2)
                    for k in range(0, min_len):
                        vector1 = numpy.array(vectors_1[k].split(" ")).reshape(1, -1)
                        vector2 = numpy.array(vectors_2[k].split(" ")).reshape(1, -1)
                        euclid_dis = (float)(euclidean_distances(vector1, vector2))
                        if (max_dis < euclid_dis):
                            max_dis = euclid_dis
                        sim_value_1 = (float)(sim_value_1 + euclid_dis)
                        sim_count = sim_count + 1
        sim_value_1 = (float)(sim_value_1 / sim_count)
        sim_value_1 = 1.0 - (float)(sim_value_1 / max_dis)
        print abs(sim_value_1)
        final_sim = max(final_sim, abs(sim_value_1))
        print "Similarity Value"
        print final_sim
        return final_sim
    else:
        sim_value_1 = 0
        sim_count = 0
        final_sim = 0.0
        max_dis = 0.0001
        frame_range = v1Range[1] - v1Range[0] + 1
        for i in range(0, frame_range):
            for j in range(1, num_cells + 1):
                print "Comparing frames " + str(v1Range[0] + i) + "  " + str(v2Range[0] + i)
                vectors_1 = dict1.get(str(v1Range[0] + i) + ',' + str(j), ["0 0 0 0"])
                vectors_2 = dict2.get(str(v2Range[0] + i) + ',' + str(j), ["0 0 0 0"])
                len_1 = len(vectors_1)
                len_2 = len(vectors_2)
                min_len = min(len_1, len_2)
                for k in range(0, min_len):
                    vector1 = numpy.array(vectors_1[k].split(" ")).reshape(1, -1)
                    vector2 = numpy.array(vectors_2[k].split(" ")).reshape(1, -1)
                    euclid_dis = (float)(euclidean_distances(vector1, vector2))
                    if (max_dis < euclid_dis):
                        max_dis = euclid_dis
                    sim_value_1 = (float)(sim_value_1 + euclid_dis)
                    sim_count = sim_count + 1
        sim_value_1 = (float)(sim_value_1 / sim_count)
        sim_value_1 = 1.0 - (float)(sim_value_1 / max_dis)
        print abs(sim_value_1)
        final_sim = max(final_sim, abs(sim_value_1))

        print "Similarity Value"
        print final_sim
        return final_sim