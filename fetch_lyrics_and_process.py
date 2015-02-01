import crawler
import embed
import sys
import pickle

with open(sys.argv[1]) as f:
  artists = [l.strip() for l in f]
songs = []

for a in artists:
  songs += crawler.getLyrics(a)

with open(sys.argv[1] + ".songs_pickle", "w") as fout:
  pickle.dump(songs, fout)

# Gets a map from artist then word to word occurrence
lyrics_map = crawler.processLyrics(songs)

with open(sys.argv[1] + ".lyrics_map_pickle", "w") as fout:
  pickle.dump(lyrics_map, fout)
