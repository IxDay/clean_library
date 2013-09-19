# -*- coding: utf-8 -*-

from path import path
import re
import errno
import mimetypes
import sys
import os

tv_show_regex = [
    re.compile(
        '(?P<name>.*?)(s|season|saison|\s)\s*?(?P<season>\d+)(e|x)(?P<episode>\d+).*?',
        re.IGNORECASE),
    re.compile(
        '(?P<name>.*?)(s|season|saison)\s*?(?P<season>\d+).*?',
        re.IGNORECASE),
    re.compile('(?P<episode>\d+).*?',re.IGNORECASE),
]

music_regex = [
    re.compile('(?P<artist>.*?)\s-\s(?P<album>.*)',re.IGNORECASE),
]

movie_regex = []


name_sanitize_regex = [
    re.compile('\W*\d{4}\W*',re.IGNORECASE),
    re.compile('\W*\d{4}\W*',re.IGNORECASE),
    re.compile('\(\d{4}\)',re.IGNORECASE),
    re.compile('.*?VOSTFR.*?',re.IGNORECASE),
    re.compile('.*?FLAC.*?',re.IGNORECASE),
    re.compile('.*?WEB.*?',re.IGNORECASE),
    re.compile('-',re.IGNORECASE),
    re.compile('.*?DVDRIP.*?',re.IGNORECASE),
    re.compile('.*?MULTI.*?',re.IGNORECASE),    
    re.compile('.*?MHD.*?',re.IGNORECASE),
    re.compile('.*?720.*?',re.IGNORECASE),
    re.compile('.*?VFF.*?',re.IGNORECASE),
    re.compile('.*?FRENCH.*?',re.IGNORECASE),
    re.compile('.*?264.*?',re.IGNORECASE),
    re.compile('.*?AAC.*?',re.IGNORECASE),
    re.compile('.*?BRRIP.*?',re.IGNORECASE),
    re.compile('.*?BDRIP.*?',re.IGNORECASE),
    re.compile('FR',re.IGNORECASE),
]


def sanitize_name(name):
    def is_pattern_word(word,patterns):
        for r in patterns:
            if r.match(word):
                return True
        return False

    words = name.replace('.',' ').replace('_',' ').split()

    for i,word in enumerate(words):
        if not is_pattern_word(word,name_sanitize_regex):
            break

    words = words[i:]

    #remove the end of the name if a trash word is caught
    words_result = []
    for word in words:    
        if is_pattern_word(word,name_sanitize_regex):
            break

        words_result.append(word.title())
    
    return "_".join(words_result)


def sanitize_number(number):
    if len(number) > 1:
        return number
    else:
        return "0" + number


def compute_tv_show_name(filename):
    result = tv_show_regex[0].match(filename.name)
    if result:
        return result.group('name'), result.group('season'), result.group('episode')
    
    result         = tv_show_regex[1].match(filename.parent.name)
    result_episode = tv_show_regex[2].match(filename.name)
    
    if result and result_episode:        
        return result.group('name'), result.group('season'), result_episode.group('episode')


def make_link(source,target):    
    try:        
        source.symlink(target)
        return target
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        

def is_tv_show(media):
    results = []
    if media.isfile():
        result = compute_tv_show_name(media)
        if result:
            results.append((result,media))
    else:        
        for f in media.walkfiles():
            result = compute_tv_show_name(f)
            if result:         
                results.append((result,f))        
    return results


def compute_music_name(filename):
    result = music_regex[0].match(filename.name)    
    if result:        
        return result.group('artist'), result.group('album')

  
def guess_type(media):
    def clean_type(filename):
        mime = mimetypes.guess_type(filename)[0]
        if mime:
            mime = mime.split('/')[0]

        return mime

    mimes = []
    if media.isdir():
        for f in media.walkfiles():
            mimes.append(clean_type(f))
    if media.isfile():
        mimes.append(clean_type(media))
    
    return mimes        


def tv_shows(media):    
    results = is_tv_show(media)
    if not results:
        return
    
    links = []
    for result,filename in results:        
        show_name      = sanitize_name(result[0])
        season_number  = sanitize_number(result[1])
        episode_number = sanitize_number(result[2])

        name = show_name + '_S' + season_number + 'E' + episode_number + filename.ext

        directory = TV_SHOWS_DIR.joinpath(show_name,'Season_'+ season_number)
        directory.makedirs_p()

        links.append(make_link(filename,directory / name))
        
    return links


def movies(media):
    links = []
    if media.isdir():
        name = sanitize_name(media.basename())
        directory = MOVIES_DIR / name
        directory.makedirs_p()
        
        for movie in media.walkfiles():
            name = sanitize_name(movie.namebase)
            links.append(directory.joinpath(name + movie.ext))
            make_link(movie, links[-1])
    else:
        name = sanitize_name(media.namebase)
        directory = MOVIES_DIR / name
        directory.makedirs_p()
        links.append(directory.joinpath(name + media.ext))
        make_link(media, links[-1])
          
    return links


def videos(media):
    links = tv_shows(media)
    if not links:
        links = movies(media)
    return links


def musics(filename):
    result = compute_music_name(filename)

    if not result:
        return

    artist = sanitize_name(result[0])
    album = sanitize_name(result[1]) 

    if not album:
        album = artist
        artist = 'Various_Artists'

    directory = MUSICS_DIR / artist
    directory.makedirs_p()
    return make_link(filename, directory / album)
    

def miscellaneous(media):
    return [make_link(media,MISC_DIR / media.basename())]


def compute_name(media):
    mimes = guess_type(media)
    TV_SHOWS_DIR.makedirs_p()
    MOVIES_DIR.makedirs_p()
    MUSICS_DIR.makedirs_p()

    if 'video' in mimes:
        links = videos(media)
    elif 'audio' in mimes:
        links = musics(media)
    else:
        links = miscellaneous(media)

    return links
    

if __name__ == "__main__":
    DATA_TORRENT_DIR = path(os.environ['DATA_TORRENT_DIR'])
    TV_SHOWS_DIR     = path(os.environ['TV_SHOWS_DIR'])
    MOVIES_DIR       = path(os.environ['MOVIES_DIR'])
    MUSICS_DIR       = path(os.environ['MUSICS_DIR'])
    MISC_DIR         = path(os.environ['MISC_DIR'])


    TV_SHOWS_DIR.makedirs_p()
    MOVIES_DIR.makedirs_p()
    MUSICS_DIR.makedirs_p()
    MISC_DIR.makedirs_p()


    if len(sys.argv) == 1:
        for media in DATA_TORRENT_DIR.listdir():
            compute_name(media)
    else:
        compute_name(path(sys.argv[1]))


    
