import asyncio

import discord

import source


class MusicQueue:
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False
        self.voice_channel = None

    async def join_channel(self, ctx):
        self.voice_channel = ctx.author.voice.channel
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client is None:
            await self.voice_channel.connect()

    def add_to_queue(self, ctx, url):
        self.queue.append((ctx, url))
        if not self.is_playing:
            self.bot.loop.create_task(self.play_next())

    async def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True
            ctx, url = self.queue.pop(0)
            await self.join_channel(ctx)

            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: self.bot.loop.create_task(self.play_next()))
        else:
            self.is_playing = False
            if self.voice_channel:
                await self.voice_channel.disconnect()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
music_queue = MusicQueue(client)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


async def play_music(channel_id: int, source_path: str, title: str):
    print("Start")

    channel = client.get_channel(channel_id)

    vc = await channel.connect()

    vc.play(discord.FFmpegPCMAudio(source_path, executable="ffmpeg.exe"), after=lambda e: print("Finished Song"))
    await client.change_presence(activity=discord.Activity(name=f"Song: {title}", type=discord.ActivityType.listening))

    while vc.is_playing():
        await asyncio.sleep(1)

    await vc.disconnect()


@client.event
async def on_message(message):
    videos = source.manager.youtube_search(message.content)

    dw_name = source.manager.download_video(f"https://youtube.com/watch?v={videos[0]['videoId']}")

    music_queue.add_to_queue(message, dw_name)
    await asyncio.sleep(1)


def run_bot(token: str):
    print("Starting bot....")
    client.run(token)
