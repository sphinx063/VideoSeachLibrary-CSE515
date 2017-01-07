import os
import imageio
from operator import itemgetter

import histogram_similarity as histsim
import sift_vector_similarity as siftsim
import motion_vector_similarity as mvectsim
import overall_similarity as overallsim

rootDir = "./P2DemoVideos"
chst = "FinalData.chst"
sift = "FinalData.sift"
mvect = "FinalData.mvect"
resolution = 2

def subsequence_search(inputvideo, frame_start, frame_end, k, method):
    videoNames = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if fname.endswith(".mp4"):
                videoNames.append(os.path.join(rootDir, fname))
    videoNames.remove(os.path.join(rootDir, inputvideo))

    result = {}
    len_of_seq = frame_end - frame_start + 1
    for video in videoNames:
        vid = imageio.get_reader(video, 'ffmpeg')
        num_frames = vid._meta['nframes'] - 1
        for i in range(1, num_frames - len_of_seq + 2):
            start = i
            end = i + len_of_seq - 1
            src_frame_range = [frame_start, frame_end]
            dst_frame_range = [start, end]
            tokens = video.split("/")
            video_name = tokens[len(tokens) - 1]
            print "Video name " + video_name + " Frames - " + str(start) + " , " + str(end)
            result[video + "," + str(start) + "," + str(end)] = \
                computeSimilarityUsingMethod(inputvideo, video_name, src_frame_range, dst_frame_range, method)
            print "Similarity " + str(result[video + "," + str(start) + "," + str(end)])

    result = sorted(result.items(), key=itemgetter(1), reverse=True)
    index = k

    print "*******************************"
    print result[:k]
    print "*******************************"

    for item in result:
        tokens = item[0].split(',')
        reader = imageio.get_reader(tokens[0])
        writer = imageio.get_writer("similar"+str(index-k+1)+".mp4", fps=reader.get_meta_data()['fps'])
        frame_index = 1
        for im in reader:
            if frame_index >= int(tokens[1]) and frame_index <= int(tokens[2]):
                writer.append_data(im[:, :, 1])
            frame_index = frame_index + 1
        writer.close()
        reader.close()
        index = index-1
        if index <= 0:
            break


def computeSimilarityUsingMethod(inputvideo, video_name, src_frame_range, dst_frame_range, method):
    if method is "chst_L1":
        return histsim.computeSimilarityL1Hist(inputvideo, video_name, chst, resolution, src_frame_range, dst_frame_range)
    elif method is "chst_L2":
        return histsim.computeSimilarityL2Hist(inputvideo, video_name, chst, resolution, src_frame_range, dst_frame_range)
    elif method is "sift_Cos":
        return siftsim.computeSimilarityCosineSift(inputvideo, video_name, sift, resolution, src_frame_range, dst_frame_range)
    elif method is "sift_L2":
        return siftsim.computeSimilarityL2Sift(inputvideo, video_name, sift, resolution, src_frame_range, dst_frame_range)
    elif method is "mvect_Cos":
        return mvectsim.computeSimilarityCosineMvect(inputvideo, video_name, mvect, resolution, src_frame_range, dst_frame_range)
    elif method is "mvect_L2":
        return mvectsim.computeSimilarityL2Mvect(inputvideo, video_name, mvect, resolution, src_frame_range, dst_frame_range)
    elif method is "all_Eq":
        return overallsim.computeSimilarityAllEq(inputvideo, video_name, chst, sift, mvect, resolution, src_frame_range, dst_frame_range)
    elif method is "all_Diff":
        return overallsim.computeSimilarityAllDiff(inputvideo, video_name, chst, sift, mvect, resolution, src_frame_range, dst_frame_range)


def initReducedSpaceInputFiles():
    chst = "FinalData.chst.pca"
    sift = "FinalData.sift.km"
    mvect = "FinalData.mvect.pca"