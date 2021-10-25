import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "23aa300a3fa84c5d981490f17df16082"
CLIENT_SECRET = "509c19fd7dda48f58b747fac74c6e89d"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/search"

year = input("Input date (YYYY-MM-DD): ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{year}")
website = response.text

soup = BeautifulSoup(website, "html.parser")
top100_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
top100_artists = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")

songs_list = [song.getText() for song in top100_songs]
artist_list = [artist.getText() for artist in top100_artists]
playlist = [{songs_list[_]: artist_list[_]} for _ in range(0, len(songs_list))]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri="http://example.com",
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()['id']
print(user_id)
song_uri = []

for dicts in playlist:
    for key, value in dicts.items():
        result = sp.search(q=f"track:{key} artist:{value}", type="track,artist")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uri.append(uri)
        except IndexError:
            print(f"{key} by {value} doesnt exist in Spotify.")

print(song_uri)

playlist_id = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
# sp.user_playlist_replace_tracks(user=user_id,playlist_id=playlist_id,tracks=song_uri)
playlist = sp.playlist_add_items(playlist_id=playlist_id['id'], items=song_uri)
