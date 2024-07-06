import discord
import os
import yt_dlp
import asyncio
from dotenv import load_dotenv

def run_bot():
        load_dotenv()
        TOKEN = os.getenv('discord_token')
        intents = discord.Intents.default()
        intents.message_content=True
        intents.voice_states=True
        client=discord.Client(intents=intents)

        queues = {}
        voice_clients={}
        yt_dl_options={'format':'bestaudio/best'}
        ytdl=yt_dlp.YoutubeDL(yt_dl_options)

        FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        @client.event
        async def on_ready():
            print(f'{client.user} puso ese cumbion')

        async def play_next(ctx,*,link):
            if queues[ctx.guild.id] != []:
                link=queues[ctx.guild.id].pop(0)
                await play(ctx,link=link)

        @client.command(name="play")
        async def play(ctx,*,link):
            try:
                voice_client =await ctx.author.voice.channel.connect()
                voice_clients[voice_client.guild.id]=voice_client 
            except Exception as e:
                print(e)

            try:
                url=link

                loop=asyncio.get_event_loop()
                data=await loop.run_in_executor(None,lambda:ytdl.extract_info(url,download=False))

                song=data['url']
                
                if voice_clients[ctx.guild.id].isplaying():
                    queues[ctx.guild.id].push(ctx)
                else:
                    player=discord.FFmpegOpusAudio(song,**FFMPEG_OPTIONS)
                    voice_clients[ctx.guild.id].play(player,after=lambda e:asyncio.run_coroutine_threadsafe(play_next(ctx),client.loop))
            except Exception as e:
                print('ERROR EN PLAY')
                print(e)
            
        @client.command(name="pause")
        async def pause(ctx):
            try:
                voice_clients[ctx.guid.id].pause()
            except Exception as e:
                print('ERROR EN PAUSA')
                print(e)

        @client.command(name="resume")
        async def resume(ctx):
            try:
                voice_clients[ctx.guid.id].resume()
            except Exception as e:
                print('ERROR EN RESUME')
                print(e)

        @client.command(name="stop")
        async def stop(ctx):
            try:
                voice_clients[ctx.guild.id].stop()
                await voice_clients[ctx.guild.id].disconnect()
            except Exception as e:
                print('ERROR EN STOP')
                print(e)   
        client.run(TOKEN)    
""""
        @client.event
        async def on_message(message):
            if message.content.startswith("?play"):
                try:
                    voice_client =await message.author.voice.channel.connect()
                    voice_clients[voice_client.guild.id]=voice_client 
                except Exception as e:
                    print(e)

                try:
                    url=message.content.split()[1]

                    loop=asyncio.get_event_loop()
                    data=await loop.run_in_executor(None,lambda:ytdl.extract_info(url,download=False))

                    song=data['url']
                    player=discord.FFmpegOpusAudio(song,**FFMPEG_OPTIONS)

                    voice_clients[message.guild.id].play(player)
                except Exception as e:
                    print('ERROR EN PLAY')
                    print(e)
            if message.content.startswith("?pause"):
                try:
                    voice_client[message.guid.id].pause()
                except Exception as e:
                    print('ERROR EN PAUSA')
                    print(e)
            if message.content.startswith("?resume"):
                try:
                    voice_client[message.guild.id].resume()
                except Exception as e:
                    print('ERROR EN RESUME')
                    print(e)
            if message.content.startswith("?stop"):
                try:
                    voice_client[message.guild.id].stop()
                    await voice_clients[message.guild.id].disconnect()
                except Exception as e:
                    print('ERROR EN STOP')
                    print(e)
                    
intents=discord.Intents.default()
intents.message_content=True
intents.voice_states=True

FFMPEG_OPTIONS={'options':'-vn'}
YDL_OPTIONS={'format':'bestaudio/best','noplaylist':True}



class MusicBot(commands.Cog):
    def __init__(self,client):
        self.client=client
        self.queue=[]

    @commands.command()
    async def play(self,ctx,*,search):
        voice_channel=ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("No estas en ningun canal D:")
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info=ydl.extract_info(f"ytsearch:{search}",download=False)
                if 'entries' in info:
                    info=info['entries'][0]
                url=info['url']
                title=info['title']
                self.queue.append((url,title))
                await ctx.send(f'Agregado a la lista:**{title}**')

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self,ctx):
        if self.queue:
            url,title=self.queue.pop(0)
            source=await discord.FFmpegAudio.from_probe(url,**FFMPEG_OPTIONS)
            ctx.voice_client.play(source,after=lambda _:self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Ahora escuchando **{title}**')
        elif not ctx.voice_client.is_playing():
            await ctx.send('La cola esta vacia!')

    @commands.command()
    async def skip(self,ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Saltando cancion')


client=commands.Bot(command_prefix=">",intents=intents)


async def on_ready():
    print(f'{client.user} is connected to the following server:\n')
    for server in client.guilds:
        print(f'{server.name}(id: {server.id})')


async def main():
    os.getenv('discord_token')
    await client.add_cog(MusicBot(client))
    await client.run('')

"""


        