import urllib2
import json
import HTMLParser
import re, operator

from contextlib import closing
from selenium.webdriver import Firefox

artist_names = []

with open("artist_names.txt", "r") as artist_file:
    artist_names = artist_file.readlines()

print artist_names

with closing(Firefox()) as browser:
    for cur_artist in artist_names:
        cur_artist = cur_artist.strip()
        print "Starting histogram for " + cur_artist
        url = "http://lyrics.wikia.com/api.php?func=getArtist&artist=" + cur_artist + "&fmt=realjson"
        print url
        artistPage = urllib2.urlopen(url)
        artistAlbums = json.load(artistPage)['albums']
        songs = []
        words = {}

        for curAlbum in artistAlbums:
            for curSong in curAlbum['songs']:
                songs.append(curSong)

            for curSong in songs:
                print "Loading song " + curSong
                browser.get("http://lyrics.wikia.com/" + cur_artist + ":" + curSong)
                lyricbox = browser.find_elements_by_class_name("lyricbox")
                
                try:
                    curWords = lyricbox[0].text.split("\n")
                except IndexError:
                    continue

                for curLine in curWords:
                    splitWords = curLine.split(" ")

                    for curWord in splitWords:
                        if words.has_key(curWord):
                            words[curWord] += 1
                        else:
                            words[curWord] = 1

        sorted_words = sorted(words.items(), key=operator.itemgetter(1))

        with open(cur_artist + ".json", "w") as artist_out_file:
            json.dump(sorted_words, artist_out_file)

        print sorted_words

