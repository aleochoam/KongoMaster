from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import secrets
import json


def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    names = []
    for track in results["items"]:
        name = track["track"]["name"]
        artist = track["track"]["artists"][0]["name"]
        names.append(name + " " + artist)
    return names


client_credentials_manager = SpotifyClientCredentials(
                    client_id=secrets.spotify_client_id,
                    client_secret=secrets.spotify_client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_url = "spotify:user:alfred953:playlist:558HrHFxBb3Ph7NZaECKfV"
playlist_data = playlist_url.split(":")
playlist_username = playlist_data[2]
playlist_id = playlist_data[4]

print("Username: " + playlist_username)
print("id: " + playlist_id)

data = get_playlist_tracks(playlist_username, playlist_id)
print(json.dumps(data, indent=4, sort_keys=True))
