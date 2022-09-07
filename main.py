from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class_name ="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
date = input("Which year do you want to travel to? Type the date in format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("h3", id="title-of-a-story", class_=class_name)
song_names = [song.getText().strip('\n') for song in song_names_spans]
print(song_names)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id="395d6fa0a9934c5fbf25bb00720cef68",
        client_secret="3942bf57425f4b9bb26f8b8b0a5fd2d5",
        redirect_uri="https://example.com/",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
# year = date.split("-")[0]
target_year = int(date.split("-")[0])
year = str(f"{target_year - 1}-{target_year + 1}")

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", collaborative=False,public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)