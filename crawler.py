import urllib2
import json
import HTMLParser
import re, operator

from contextlib import closing
from selenium.webdriver import Firefox

artistName = "Cake"
artistPage = urllib2.urlopen("http://lyrics.wikia.com/api.php?func=getArtist&artist=" + artistName + "&fmt=realjson")
artistAlbums = json.load(artistPage)['albums']
songs = []
words = {}

for curAlbum in artistAlbums:
    for curSong in curAlbum['songs']:
        songs.append(curSong)

with closing(Firefox()) as browser:
    for curSong in songs:
        print "Loading page..."
        browser.get("http://lyrics.wikia.com/" + artistName + ":" + curSong)
        print "Page loaded..."
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

print sorted_words

