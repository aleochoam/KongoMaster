import discord
from discord.ext import commands
import youtube_dl
from secrets import TOKEN

client = commands.Bot(command_prefix="oe ")

# players of each server
players = {}

# queues of each server
queues = {}


def check_queue(id):
    if queues[id] != []:
        player = queues.pop(0)
        players[id] = player
        player.start()


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
async def play(ctx, url):
    server = ctx.message.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
    else:
        channel = ctx.message.author.voice.voice_channel
        voice_client = await client.join_voice_channel(channel)

    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


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


@client.command(pass_context=True)
async def add(ctx, url):
    server = ctx.message.server
    server = ctx.message.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
    else:
        channel = ctx.message.author.voice.voice_channel
        voice_client = await client.join_voice_channel(channel)
    player = await voice_client.create_ytdl_player(
                        url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]

    await client.say("Video queued")


client.run(TOKEN)
