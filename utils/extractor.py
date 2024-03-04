#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	A script to download videos and extract audio for the CORDI project
	Sina Ahmadi (ahmadi.sina@outlook.com)
	Created on 03/11/2021
"""
from pytube import YouTube
import moviepy.editor as mp

def download_video(ID, URL):
	print("==============================", ID)
	print("Downloading...")
	yt_url = YouTube(URL)
	yt_vid = yt_url.streams.filter(file_extension="mp4").first()
	mp4file = yt_vid.download(output_path="video", filename="%s.mp4"%ID)

	print("Extracting...")
	my_clip = mp.VideoFileClip("video/%s.mp4"%ID)
	my_clip.audio.write_audiofile("video/%s.wav"%ID)
	print("Saved!")

if __name__ == '__main__':
	# with open("CORDI_description.tsv", "r") as f:
	# 	sheet = f.read().splitlines()[1:]

	# for i in sheet:
	# 	ID, YouTube_URL = i.split("\t")[0], i.split("\t")[9]
	# 	if "http" in YouTube_URL:
	# 		download_video(ID, YouTube_URL)
	ID, YouTube_URL = "164", "https://www.youtube.com/watch?v=ym0S7QSc4S4"
	if "http" in YouTube_URL:
		download_video(ID, YouTube_URL)