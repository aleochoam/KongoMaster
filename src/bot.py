from discord.ext import commands
import secrets
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

client = commands.Bot(command_prefix="oe ")

# players of each server
players = {}

# queues of each server
queues = {}

# Spotify client
client_credentials_manager = SpotifyClientCredentials(
                    client_id=secrets.spotify_client_id,
                    client_secret=secrets.spotify_client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def check_queue(id):
    print("por aca")
    if queues[id] != []:
        player = queues.pop(0)
        players[id] = player
        player.start()


def get_spotify_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    names = []
    for track in results["items"]:
        name = track["track"]["name"]
        artist = track["track"]["artists"][0]["name"]
        names.append(name + " " + artist)
    return names


def get_link_if_search(textToSearch):
    if "youtube.com" not in textToSearch:
        query = quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})[0]
        return('https://www.youtube.com' + vid['href'])

    else:
        return textToSearch


async def get_voice_client(ctx):
    server = ctx.message.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
    else:
        channel = ctx.message.author.voice.voice_channel
        voice_client = await client.join_voice_channel(channel)
    return voice_client


@client.event
async def on_ready():
    print("Kongo Master Ready!!")


@client.command()
async def ping():
    await client.say("Pong!")


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, *text):
    text = " ".join(text)
    print("Buscando: " + text)
    server = ctx.message.server
    voice_client = await get_voice_client(ctx)

    url = get_link_if_search(text)
    player = await voice_client.create_ytdl_player(
        url,
        after=lambda: check_queue(server.id))

    players[server.id] = player

    await client.say("Zumbando: " + url)
    player.start()


@client.command(pass_context=True)
async def add(ctx, text):
    text = " ".join(text)
    server = ctx.message.server
    voice_client = await get_voice_client(ctx)
    url = get_link_if_search(text)
    player = await voice_client.create_ytdl_player(
                        url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]

    await client.say("Video queued")


@client.command(pass_context=True)
async def spotify(ctx, uri):
    server = ctx.message.server

    playlist_data = uri.split(":")
    playlist_username = playlist_data[2]
    playlist_id = playlist_data[4]

    tracks = get_spotify_playlist_tracks(playlist_username, playlist_id)
    voice_client = await get_voice_client(ctx)

    for i, track in enumerate(tracks):
        print("Searching: " + track)
        url = get_link_if_search(track)
        player = await voice_client.create_ytdl_player(
                        url, after=lambda: check_queue(server.id))

        if i == 0:
            player.start()

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
    await client.say("La playlist a sido procesada será reproducida")


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()


@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

client.run(secrets.TOKEN)
