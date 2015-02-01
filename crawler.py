import urllib2
import json
import HTMLParser
import re, operator
import sys
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import string
import unicodedata

from contextlib import closing
from selenium.webdriver import Firefox

_digits = re.compile('\d')
stopwords = set(nltk.corpus.stopwords.words())


tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                          if unicodedata.category(unichr(i)).startswith('P'))

def is_punctuation(text):
      return len(text.translate(tbl)) == 0

def contains_digits(s):
    return bool(_digits.search(s))

def is_stopword(s):
    return s in stopwords

class Song:
    def __init__(self, artist=None, album=None, year=None, song=None, lyrics=None):
        self.artist = artist
        self.album = album
        self.year = year
        self.song = song
        self.lyrics = lyrics

def getLyrics(artist_name):
    # Crawl all lyrics for this artist. Return a list of Song class instances,
    # which each contain fields for the artist name, album name, song name,
    # and lyrics (text).
    songs = []
    with closing(Firefox()) as browser:
        artist_name = artist_name.strip()
        print "Starting histogram for " + artist_name
        url = "http://lyrics.wikia.com/api.php?func=getArtist&artist=" + artist_name + "&fmt=realjson"
        print url
        artistPage = urllib2.urlopen(url)

        try:
            artistAlbums = json.load(artistPage)['albums']
        except ValueError:
            print "Albums could not be decoded"
            return songs

        print artist_name, "has", len(artistAlbums), "albums"

        if len(artistAlbums) == 0:
            print "Skipping", artist_name
            return songs

        for curAlbum in artistAlbums:
            if 'year' in curAlbum:
                year = curAlbum['year']
            else:
                year = None
            for curSong in curAlbum['songs']:
                print "Loading song " + curSong
                browser.get("http://lyrics.wikia.com/" + artist_name + ":" + curSong)
                lyricbox = browser.find_elements_by_class_name("lyricbox")
                try:
                    songs.append(Song(
                        artist=artist_name,
                        album=curAlbum['album'],
                        year=year,
                        song=curSong,
                        lyrics=lyricbox[0].text))
                except IndexError:
                    continue
    return songs

def processLyrics(songs):
    # Process the lyrics from a list of Song class instances and return a
    # dictionary that maps artist name to a dictionary that maps word to
    # number of occurrences. So d[artist][word] is the number of times artist
    # used word in this set of songs.
    lyrics_map = {}

    for song in songs:
        if song.artist not in lyrics_map:
            lyrics_map[song.artist] = {}
        # We may or may not want to switch this for sent_tokenizer.
        curWords = song.lyrics.split("\n")

        for curLine in curWords:
            splitWords = [w.lower() for w in nltk.word_tokenize(curLine)]

            for curWord in splitWords:
                if (is_stopword(curWord) or is_punctuation(curWord)
                    or contains_digits(curWord)):
                    continue 
                if curWord in lyrics_map[song.artist]:
                    lyrics_map[song.artist][curWord] += 1
                else:
                    lyrics_map[song.artist][curWord] = 1
    return lyrics_map
