import os
import json
import operator
import sys

class Embedder():
    def __init__(self):
        print "initialized"
        self.artist_freqs = {}
        self.word_freqs = {}
        self.artist_histograms = {}

    def ImportArtist(self, artist_name, histogram):
        if self.artist_freqs.has_key(artist_name):
            print "Duplicate artist for", artist_name, "- skipping?"
            return

        self.artist_freqs[artist_name] = sum(y for x, y in list(histogram))
        self.artist_histograms[artist_name] = histogram
        #print artist_name, histogram, self.artist_histograms
        #sys.exit()


        for cur_word, cur_count in list(histogram):
            if self.word_freqs.has_key(cur_word):
                self.word_freqs[cur_word] += cur_count
            else:
                self.word_freqs[cur_word] = cur_count

    def PrintResults(self):
        artist_lookup = []
        word_lookup = []

        sorted_freqs = sorted(self.artist_freqs.items(), key=operator.itemgetter(1))[::-1]

        with open("artist_ids.txt", "w") as artist_ids:
            idx = 0
            for tup in sorted_freqs:
                artist_lookup.append(str(tup[0]))
                artist_ids.write(str(idx) + "<SEP>" + str(tup[0]) + "<SEP>" + str(tup[1]) + "\n")
                idx+=1

        sorted_words = sorted(self.word_freqs.items(), key=operator.itemgetter(1))[::-1]

        with open("word_ids.txt", "w") as word_ids:
            idx = 0
            for tup in sorted_words:
                word_lookup.append(str(tup[0]))
                word_ids.write(str(idx) + "<SEP>" + str(tup[0]) + "<SEP>" + str(tup[1]) + "\n")
                idx+=1

        with open("artist_histograms.txt", "w") as artist_histograms:
            idx = 0
            for cur_artist in artist_lookup:
                artist_histograms.write(str(artist_lookup.index(cur_artist)) + " ")
                for cur_word in self.artist_histograms[cur_artist]:
                    artist_histograms.write(str(word_lookup.index(cur_word[0])) + ":" + str(cur_word[1]) + " ")
                artist_histograms.write("\n")



if __name__ == "__main__":
    print "Running module as main - looking through local directory"
    embed = Embedder()

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith("json")]
    for file in files:

        print "Loading artist", file.split(".")[0]

        cur_file = open(file, "r")
        cur_json = json.load(cur_file)

        embed.ImportArtist(str(file.split(".")[0]), cur_json)
    
    embed.PrintResults()
