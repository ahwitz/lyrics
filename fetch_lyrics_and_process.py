import crawler
import embed
import sys
import pickle

def fetch_and_process_artist_file(filename):
  with open(filename) as f:
    artists = [l.strip() for l in f]
  fetch_and_process_artists(artists, filename)

def fetch_and_process_artists(artist_list, filename):
  songs = []

  for a in artist_list:
    songs += crawler.getLyrics(a)

  with open(filename + ".songs_pickle", "w") as fout:
    pickle.dump(songs, fout)

# Gets a map from artist then word to word occurrence
  lyrics_map = crawler.processLyrics(songs)

  with open(filename + ".lyrics_map_pickle", "w") as fout:
    pickle.dump(lyrics_map, fout)

if __name__ == "__main__":
  fetch_and_process_artist_file(sys.argv[1])
