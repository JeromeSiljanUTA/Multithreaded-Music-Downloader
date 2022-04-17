# Multithreaded Music Downloader

This is a multithreaded music downloader. These are the steps it takes:
 - User inputs an artists' name
 - Search for all albums (excluding EPs, singles, mixes, etc.)
 - Find all tracks in these albums
 - Download the tracks by searching for them using `youtube-dl`
 
 The downloading occurs in parallel thanks to `ThreadPoolExecuter`

## Install
Dependencies:
```
pip install musicbrainzngs
youtube-dl
```

## Run 
```
python main.py
```

*I will add more documentation later*
