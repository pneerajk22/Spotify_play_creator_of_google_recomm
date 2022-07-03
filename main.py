import selenium.webdriver.common.devtools.v85.runtime
from bs4 import BeautifulSoup
from lxml import html
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium.webdriver.common.by import By
from selenium import webdriver

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = "CLIENT_SECRET"

#-------------------------------------------------------------------------------------------------------------------------------------------------
def songs_extractor(url):
    driver_path = r"chromedriver.exe"
    # url = "https://www.google.com/search?q=english+all+time+best+songs"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    songslst = []
    for i in range(1, 40):
        try:
            xpath = f'/html/body/div[7]/div/div[7]/div[1]/div/div/div[1]/div/div[1]/g-scrolling-carousel/div[1]/div/div/a[{i}]/div/div/div[2]/div[1]'
            content = driver.find_element(By.XPATH, xpath)
            songslst.append(content.text)
        except selenium.common.exceptions.NoSuchElementException:
            print('see through index')

    with open('songs.txt', 'w') as file:
        for song in songslst:
            file.write(song + ',')
    return songslst
#-------------------------------End of Songs_extractor function--------------------------------------------------------------------------------------


def spotify_play_creater(songslst,play_name):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="https://example.com/callback",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True,
            cache_path="token.txt"
        )
    )

    user_id = sp.current_user()["id"]
    print(user_id)
    song_uris = []
    for song in songslst:
        result = sp.search(q=f"track:{song}", type="track")
        # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

    playlist = sp.user_playlist_create(user=user_id, name=f'{play_name}', public=False)
    print(playlist)

    # Adding songs found into the new playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
#------------------------this is end of spotify_play_creator function------------------------------------------------------------------------------------


conf = input('Do you want to extract song from google? if yes type (y) else (n): ')
if(conf == 'y' or conf =='Y'):
    url_in = input('Please enter url(eg:-https://www.google.com/search?q=english+all+time+best+songs): ')

    songs_extractor(url_in)

songslst = []
with open('songs.txt','r') as songs_file:
    for line in songs_file:
        for song in line.split(","):
            songslst.append(song)

print(songslst)
name = input('Please enter name for playlist: ')
spotify_play_creater(songslst,name)
