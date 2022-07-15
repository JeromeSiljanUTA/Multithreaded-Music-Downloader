import argparse
from pathlib import Path
import threading
import time
import os
import musicbrainzngs
from concurrent.futures import ThreadPoolExecutor

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)
    parser.add_argument("integers", type=int)
    args = parser.parse_args()
    file_dest = args.file_path
    num_threads = args.integers
except:
    print('\nUsage: python main.py <destination> <number of threads>')
    print('Recommended number of threads to use is 4')
    exit()

musicbrainzngs.set_useragent("Jerome's Music Scraper", "0.1", "jerome.siljan@mavs.uta.edu")

input_artist = input("Which artist are you looking for? ")

artist_id = musicbrainzngs.search_artists(input_artist)["artist-list"][0]["id"]


raw_releases = musicbrainzngs.get_artist_by_id(artist_id, 
        includes=["release-groups"], release_type=["album", "ep"])

album_list = []
album_list_id = []


for release_group in raw_releases["artist"]["release-group-list"]:
    album_list.append(release_group["title"])

def add_tracks(title_num, discography, input_artist, album_list):
    discography.append([album_list[title_num]])
    album_id = (musicbrainzngs.search_releases(artist=input_artist, release=album_list[title_num], limit=1))["release-list"][0]["id"]
    raw_tracks_list = musicbrainzngs.get_release_by_id(album_id, includes=["recordings"])
    tracks_list = (raw_tracks_list["release"]["medium-list"][0]["track-list"])
    for track in tracks_list:
        discography[title_num].append(track["recording"]["title"])

discography = []

def ytdl(song_name, album_name):
    args = input_artist + ' ' + song_name
    cmd = 'youtube-dl --extract-audio --audio-format mp3 --output "'
    cmd += str(file_dest)
    cmd += '/' + album_name + '/'
    cmd += '/' + song_name 
    cmd += '.%(ext)s" "ytsearch:'
    cmd += args + ' audio"'
    os.system(cmd)
    cmd = 'id3v2 --artist "'
    cmd += input_artist + '" --album "'
    cmd += album_name + '" --song "'
    cmd += song_name + '"'
    cmd += ' "' + str(file_dest)
    cmd += '/' + album_name + '/'
    cmd += song_name + '.mp3"'
    #print('\n\n' + cmd + '\n\n')
    os.system(cmd)


print('\nType the numbers of the albums you want to download: ')

for num in range(len(album_list)):
    add_tracks(num, discography, input_artist, album_list)
    print(str(num) + '. ' + album_list[num])

print('-----------------------------------------------------')
desired_albums = input('>> ')
arr_desired_albums = desired_albums.split()

album_index_num = 0
executor = ThreadPoolExecutor(max_workers=num_threads)
for album in discography:
    if str(album_index_num) in arr_desired_albums:
        os.mkdir(str(file_dest) + '/' + str(album_list[album_index_num]))
        for song in album:
            executor.submit(ytdl, song_name=song, album_name=album_list[album_index_num])

    album_index_num += 1
