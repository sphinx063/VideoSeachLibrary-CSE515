// ffmpegTest.cpp : Defines the entry point for the console application.
//

/*
The following program extracts the motion vector of the given data files.
*/
#include "stdafx.h"
#include "conio.h"
#include "atlstr.h"
#include <windows.h>
#include <tchar.h>
#include <stdio.h>
#include <strsafe.h>
#include <iostream>
#include <string.h>
#include <fstream>
#include <vector>
#include <math.h>  
#pragma comment(lib, "User32.lib")
using namespace std;

extern "C"
{
#include <libavutil/motion_vector.h>
#include <libavformat/avformat.h>
# pragma comment (lib, "avformat.lib")
}
static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *video_dec_ctx = NULL;
static AVStream *video_stream = NULL;
static char *src_filename = NULL;
vector<string> fileNames;
static int video_stream_idx = -1;
static AVFrame *frame = NULL;
static AVPacket pkt;
static int video_frame_count = 0;
static int file_no = 0;
static int r = 0;
std::ofstream myfile;
static int decode_packet(int *got_frame, int cached)
{
	
	int decoded = pkt.size;

	*got_frame = 0;

	if (pkt.stream_index == video_stream_idx) {
		int ret = avcodec_decode_video2(video_dec_ctx, frame, got_frame, &pkt);
		if (ret < 0) {
			//TODO : Fix the below line
			//fprintf(stderr, "Error decoding video frame (%s)\n", av_err2str(ret));
			return ret;
		}

		if (*got_frame) {
			int i;
			AVFrameSideData *sd;

			video_frame_count++;
			sd = av_frame_get_side_data(frame, AV_FRAME_DATA_MOTION_VECTORS);
			int frameW = frame->width;
			int frameH = frame->height;
			int cellW = frameW / r;
			int cellH = frameH / r;
			if (sd) {
				const AVMotionVector *mvs = (const AVMotionVector *)sd->data;
				
				
				for (i = 0; i < sd->size / sizeof(*mvs); i++) {
					const AVMotionVector *mv = &mvs[i];
					char buffer[500];
					//printf("%d %d %d %d %d %d %d %d 0x%\n",PRIx64,"\n",
					printf("%d %d %d %d %d %d %d %d %d\n",
						video_frame_count, mv->source,
						mv->w, mv->h, mv->src_x, mv->src_y,
						mv->dst_x, mv->dst_y, mv->flags);
					//write to fil
					int cellC = (mv->dst_x) / cellW;
					int cellR = (mv->dst_y) / cellH;
					int cellCount = r*cellR + cellC+1;
					//Write the motion vector values to the output file.
					sprintf(buffer, "%d %d %d %d %d %d %d %d %d %d\n",
							file_no,video_frame_count,cellCount, mv->source,
							mv->w, mv->h, mv->src_x, mv->src_y,
							mv->dst_x, mv->dst_y);
					myfile << buffer;
					
					printf("----------------------------------------------------------------------------\n");

					//printf("I am Here %d\n",i);
				}
			}
		}
	}

	return decoded;
}

static int open_codec_context(int *stream_idx,
	AVFormatContext *fmt_ctx, enum AVMediaType type)
{
	int ret;
	AVStream *st;
	AVCodecContext *dec_ctx = NULL;
	AVCodec *dec = NULL;
	AVDictionary *opts = NULL;

	ret = av_find_best_stream(fmt_ctx, type, -1, -1, NULL, 0);
	if (ret < 0) {
		fprintf(stderr, "Could not find %s stream in input file '%s'\n",
			av_get_media_type_string(type), src_filename);
		return ret;
	}
	else {
		*stream_idx = ret;
		st = fmt_ctx->streams[*stream_idx];

		/* find decoder for the stream */
		dec_ctx = st->codec;
		dec = avcodec_find_decoder(dec_ctx->codec_id);
		if (!dec) {
			fprintf(stderr, "Failed to find %s codec\n",
				av_get_media_type_string(type));
			return AVERROR(EINVAL);
		}

		/* Init the video decoder */
		av_dict_set(&opts, "flags2", "+export_mvs", 0);
		if ((ret = avcodec_open2(dec_ctx, dec, &opts)) < 0) {
			fprintf(stderr, "Failed to open %s codec\n",
				av_get_media_type_string(type));
			return ret;
		}
	}

	return 0;
}
//Function to get all the files in the given directory and store it in a vector
void getFiles(char *dir)
{
	WIN32_FIND_DATA ffd;
	LARGE_INTEGER filesize;
	TCHAR szDir[MAX_PATH];
	size_t length_of_arg;
	HANDLE hFind = INVALID_HANDLE_VALUE;
	DWORD dwError = 0;

	// Check that the input path plus 3 is not longer than MAX_PATH.
	// Three characters are for the "\*" plus NULL appended below.
	USES_CONVERSION;
	TCHAR szName[512];
	_tcscpy(szName, A2T(dir));
	StringCchLength(szName, MAX_PATH, &length_of_arg);
	if (length_of_arg > (MAX_PATH - 3))
	{
		printf("Directory path is too long.\n");
		return;
	}

	// Prepare string for use with FindFile functions.  First, copy the
	// string to a buffer, then append '\*' to the directory name.

	StringCchCopy(szDir, MAX_PATH, szName);
	_tprintf(szDir);
	StringCchCat(szDir, MAX_PATH, TEXT("\\*"));

	// Find the first file in the directory.

	hFind = FindFirstFile(szDir, &ffd);

	if (INVALID_HANDLE_VALUE == hFind)
	{
		printf("FindFirstFile\n");
		return;
	}

	int i = 0;
	do
	{
		if (!(ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
		{
			TCHAR file[512];
			StringCchCopy(file, MAX_PATH, szName);
			StringCchCat(file, MAX_PATH, TEXT("\\"));
			StringCchCat(file, 512, ffd.cFileName);
			fileNames.push_back(T2A(file));
			printf("filename %s \n", fileNames[i++]);
		}
	} while (FindNextFile(hFind, &ffd) != 0);
	FindClose(hFind);
}

int processFile(const char *src_filename) {
	int ret = 0, got_frame;
	av_register_all();
	if (avformat_open_input(&fmt_ctx, src_filename, NULL, NULL) < 0) {
		fprintf(stderr, "Could not open source file %s\n", src_filename);
		exit(1);
	}

	if (avformat_find_stream_info(fmt_ctx, NULL) < 0) {
		fprintf(stderr, "Could not find stream information\n");
		exit(1);
	}

	if (open_codec_context(&video_stream_idx, fmt_ctx, AVMEDIA_TYPE_VIDEO) >= 0) {
		video_stream = fmt_ctx->streams[video_stream_idx];
		video_dec_ctx = video_stream->codec;
	}

	av_dump_format(fmt_ctx, 0, src_filename, 0);

	if (!video_stream) {
		fprintf(stderr, "Could not find video stream in the input, aborting\n");
		ret = 1;
		goto end;
	}

	frame = av_frame_alloc();
	if (!frame) {
		fprintf(stderr, "Could not allocate frame\n");
		ret = AVERROR(ENOMEM);
		goto end;
	}

	printf("framenum,source,blockw,blockh,srcx,srcy,dstx,dsty,flags\n");

	/* initialize packet, set data to NULL, let the demuxer fill it */
	av_init_packet(&pkt);
	pkt.data = NULL;
	pkt.size = 0;

	/* read frames from the file */
	while (av_read_frame(fmt_ctx, &pkt) >= 0) {
		AVPacket orig_pkt = pkt;
		do {
			ret = decode_packet(&got_frame, 0);
			if (ret < 0)
				break;
			pkt.data += ret;
			pkt.size -= ret;
		} while (pkt.size > 0);
		av_packet_unref(&orig_pkt);
	}

	/* flush cached frames */
	pkt.data = NULL;
	pkt.size = 0;
	do {
		decode_packet(&got_frame, 1);
	} while (got_frame);

end:
	avcodec_close(video_dec_ctx);
	avformat_close_input(&fmt_ctx);
	av_frame_free(&frame);
	return ret < 0;

}
/*
	Please provide the values for command line arguments in the following oredr. Directory dir, resolution r, outputfile out_file.txt
*/
int main(int argc, char **argv)
{
	myfile.open(argv[3], std::ofstream::out | std::ofstream::app);

	if (argc != 4) {
		fprintf(stderr, "Usage: %s <video>\n", argv[0]);
		exit(1);
	}
	r = atoi(argv[2]);
	getFiles(argv[1]);
	//Iterate over the vector containing the file names.
	for (std::vector<string>::iterator v = fileNames.begin(); v != fileNames.end(); ++v) {
			/* std::cout << *it; ... */
		video_frame_count = 0;
		file_no++;
		processFile((*v).c_str());

	}
	myfile.close();
	
	
}


