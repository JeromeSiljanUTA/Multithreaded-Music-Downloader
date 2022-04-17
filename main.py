import threading
import time
import musicbrainzngs

musicbrainzngs.set_useragent("Jerome's Music Scraper", "0.1", "jerome.siljan@mavs.uta.edu")

#input_artist = input("Which artist are you looking for? ")
input_artist = "Maluma"

artist_id = musicbrainzngs.search_artists(input_artist)["artist-list"][0]["id"]


raw_releases = musicbrainzngs.get_artist_by_id(artist_id, 
        includes=["release-groups"], release_type=["album", "ep"])

print("Albums:")

album_list = []
album_list_id = []

for release_group in raw_releases["artist"]["release-group-list"]:
    album_list.append(release_group["title"])

def add_tracks(title_num, discography, input_artist, album_list):
    print("Tracks in " + album_list[title_num] + ":")
    discography.append([album_list[title_num]])
    album_id = (musicbrainzngs.search_releases(artist=input_artist, release=album_list[title_num], limit=1))["release-list"][0]["id"]
    raw_tracks_list = musicbrainzngs.get_release_by_id(album_id, includes=["recordings"])
    tracks_list = (raw_tracks_list["release"]["medium-list"][0]["track-list"])
    for track in tracks_list:
        print("\t" + track["recording"]["title"])
        discography[title_num].append(track["recording"]["title"])
    #print(discography[title_num])

discography = []


for num in range(len(album_list)):
    add_tracks(num, discography, input_artist, album_list)

print(discography)
