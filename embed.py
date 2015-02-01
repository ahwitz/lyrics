import os
import json
import operator

class Embedder():
    #min_frequency as parameter on initialization is the threshold to include words:
    #   if an artist says the word "frequency" 2 times in their corpus and min_frequency is 10, "frequency" will not be calculated
    def __init__(self, min_frequency):
        print "initialized"
        self.artist_freqs = {} #list of total different words used by artist with {artist:total} pairs
        self.word_freqs = {} #list of total frequencies of words throughout all input with {word:total} pairs
        self.artist_histograms = {} #artist histograms as dictionaries with {artist:histogram} pairs
        self.min_frequency = min_frequency

    def ImportArtist(self, artist_name, histogram):
        if self.artist_freqs.has_key(artist_name):
            print "Duplicate artist for", artist_name, "- skipping?"
            return

        threshold_histogram = {}
        for x, y in list(histogram):
            if y >= self.min_frequency:
                threshold_histogram[x] = y

        self.artist_freqs[artist_name] = sum(y for x, y in threshold_histogram.items())
        self.artist_histograms[artist_name] = threshold_histogram

        for cur_word, cur_count in threshold_histogram.items():
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
                for cur_word, cur_count in self.artist_histograms[cur_artist].items():
                    artist_histograms.write(str(word_lookup.index(cur_word)) + ":" + str(cur_count) + " ")
                artist_histograms.write("\n")



if __name__ == "__main__":
    print "Running module as main - looking through local directory"
    embed = Embedder(10)

    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith("json")]
    for file in files:

        print "Loading artist", file.split(".")[0]

        cur_file = open(file, "r")
        cur_json = json.load(cur_file)

        embed.ImportArtist(str(file.split(".")[0]), cur_json)
    
    embed.PrintResults()
