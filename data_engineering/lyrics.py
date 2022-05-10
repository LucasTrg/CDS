
from lyricsgenius import Genius

import pandas as pd


genius = Genius("zOlRkvee_39qOiaUkaYBhDrzb8idWU_767H4Znl38IdfoxMfFydc3ON6BLCxwahG")
genius.excluded_terms = ["(Remix)", "(Live)"]

df=pd.read_csv("data/rap_world/artists_NYC.csv")

def get_album(album_id):
    try:
        print("test")
        return genius.search_album(album_id=album_id)
    except Exception as e:

        return get_album(album_id)

def fetch_lyrics(line):
    try :
        artist_name=line["Name"]
    except Exception as e :
        print("unexpected error", e)
    try:
        artist=genius.search_artist(artist_name, sort="title", max_songs=2, per_page=50)
        songs_lyrics=[]
        release_date=[]
        for song in artist.songs:
            if song.album_id!=-1:
                album = get_album(song.album_id)
                print(album.release_date_components)
                release_date.append(album.release_date_components)
            else:
                release_date.append(-1)
            songs_lyrics.append(song.lyrics)



        return [songs_lyrics, release_date]
    except Exception as e:
        print(e)
        print("Reattempting fetching")
        return fetch_lyrics(artist_name)

df = pd.concat((df,df.apply(lambda x: pd.Series(fetch_lyrics(x), index =['lyrics', 'release']), axis = 1)), axis=1)

df.to_csv("data/lyrics/genius_v6.csv")