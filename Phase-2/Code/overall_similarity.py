import histogram_similarity as histsim
import sift_vector_similarity as siftsim
import motion_vector_similarity as mvectsim


def computeSimilarityOverallEq(video1, video2, chst, sift, features_mvect, resolution, src_frame_range, dst_frame_range):
    histSimilarity = histsim.computeSimilarityL1Hist(video1, video2, chst, resolution, src_frame_range, dst_frame_range)
    siftSimilarity = siftsim.computeSimilarityL2Sift(video1, video2, sift, resolution, src_frame_range, dst_frame_range)
    mvectSimilarity = mvectsim.computeSimilarityCosineMvect(video1, video2, features_mvect, resolution, src_frame_range, dst_frame_range)
    avgSimilarity = (histSimilarity + siftSimilarity + mvectSimilarity)/3
    return avgSimilarity


def computeSimilarityOverallDiff(video1, video2, chst, sift, features_mvect, resolution, src_frame_range, dst_frame_range):
    histSimilarity = histsim.computeSimilarityL1Hist(video1, video2, chst, resolution, src_frame_range, dst_frame_range)
    siftSimilarity = siftsim.computeSimilarityL2Sift(video1, video2, sift, resolution, src_frame_range, dst_frame_range)
    mvectSimilarity = mvectsim.computeSimilarityCosineMvect(video1, video2, features_mvect, resolution, src_frame_range, dst_frame_range)
    avgSimilarity = histSimilarity*0.1 + siftSimilarity*0.3 + mvectSimilarity*0.6
    return avgSimilarity