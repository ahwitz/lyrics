import urllib2
import json
import HTMLParser
import re, operator
import sys
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import string
import unicodedata
import bs4
from joblib import Parallel, delayed

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

def getSongLyrics(song):
    quoted_song = urllib2.quote(song.song.encode("utf-8"))
    quoted_artist_name = urllib2.quote(song.artist.encode("utf-8"))
    print "Loading song " + song.song
    lyrics_url = "http://lyrics.wikia.com/" + quoted_artist_name + ":" + quoted_song
    try:
        lyrics_page = urllib2.urlopen(lyrics_url)
    except urllib2.HTTPError as e:
        print "Skipping: " + str(e)
        return None
    lyrics_page_text = "".join(lyrics_page.readlines())
    bspage = bs4.BeautifulSoup(lyrics_page_text)
    # get the lyricbox element
    lyricbox = bspage.find(name="div", attrs={"class":"lyricbox"})
    # find all the strings in the elemnet, i.e. not tags, but
    # exclude the comments
    if lyricbox is None:
        print "No lyricbox, skipping"
        return None
    lyric_children = [_ for _ in lyricbox.children
        if isinstance(_, bs4.element.NavigableString)
        and not isinstance(_, bs4.element.Comment)]
    song.lyrics = "\n".join([l.strip() for l in lyric_children if len(l.strip()) > 0])
    return song

def getLyrics(artist_name, num_processes=1):
    # Crawl all lyrics for this artist. Return a list of Song class instances,
    # which each contain fields for the artist name, album name, song name,
    # and lyrics (text).
    artist_name = artist_name.strip()
    quoted_artist_name = urllib2.quote(artist_name.encode("utf-8"))
    print "Starting histogram for " + artist_name
    url = "http://lyrics.wikia.com/api.php?func=getArtist&artist=" + quoted_artist_name + "&fmt=realjson"
    print url
    artistPage = urllib2.urlopen(url)
    query_songs = []

    try:
        artistAlbums = json.load(artistPage)['albums']
    except ValueError:
        print "Albums could not be decoded for {}".format(artist_name)
        return []

    print artist_name, "has", len(artistAlbums), "albums"

    if len(artistAlbums) == 0:
        print "Skipping", artist_name
        return []

    for curAlbum in artistAlbums:
        if 'year' in curAlbum:
            year = curAlbum['year']
        else:
            year = None
        for song_name in curAlbum['songs']:
            query_songs.append(Song(
                artist=artist_name,
                album=curAlbum['album'],
                year=year,
                song=song_name))

    result_songs = Parallel(n_jobs=num_processes)(delayed(getSongLyrics)(song)
        for song in query_songs)
    return [s for s in result_songs if s is not None]

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
