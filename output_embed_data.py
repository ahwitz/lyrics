# coding: utf-8
import embed
import os
import pickle
embedder = embed.Embedder(10)
mapfiles = ["split_artists/" + f for f in os.listdir("split_artists/") if ".lyrics_map" in f]
for fn in mapfiles:
    with open(fn) as f:
        lyrics_map = pickle.load(f)
    for a in lyrics_map:
        embedder.ImportArtist(a, lyrics_map[a])
embedder.PrintResults()
