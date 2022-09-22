import discord
from discord.ext import commands
import asyncio
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from discord import welcome_screen, WelcomeChannel, guild, utils

intents = discord.Intents.all()
client = commands.Bot(command_prefix="\\", intents= intents)

list_ban = {}

@client.command(name="ola", help= ">>> Apenas umas apresentação")
async def ola(context):
    await context.message.channel.send("Hello World!")


#   #   # ---------- BOAS VINDAS ---------- #    #    #

@client.event
async def on_member_join(member):
   await client.get_channel().send(f"{member.name}, entrou no Contenção! Calmo Relaxo!")

#   #   # --------------------------------- #    #    #



#   #   # ---------- VOTE BAN ---------- #    #    #

@client.command(name="voteban", help=">>> Votação para kick  >  Argumento: mencionar usuario que deseja")
async def ban(context):
    user = context.message.mentions[0]
    if user.name in list_ban:
        if context.message.author.name in list_ban[user.name]:
            await context.message.channel.send("***Você já votou!***")
            print(list_ban)
        else:
            get_list = list_ban[user.name]
            get_list.append(context.message.author.name)
            list_ban[user.name] = get_list
            await context.message.channel.send("Voto em {} recebido com sucesso! Estado atual : {}/5" .format(user.name, len(list_ban[user.name])))
            print(list_ban)
            if len(list_ban[user.name]) >= 5:
                await user.kick()

    else:
        list_ban[user.name] = [context.message.author.name]
        await context.message.channel.send("Voto recebido com sucesso!")
        print(list_ban)

#   #   # ------------------------------ #    #    #



#   #   # ---------- Musica Atual Spotify ---------- #    #    #

@client.command(name="musica", help= ">>> Sua musica atual no Spotify")
async def spotify(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, discord.Spotify):
                embed = discord.Embed(
                    title = f"{user.name} agora no Spotify: ",
                    description = "Escutando: {}".format(activity.title),
                    color = 0x0291ff)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artista", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                # embed.set_footer(text="Musica iniciad em: {}".format(activity.created_at.strftime("%H:%M")))
                m1, s1 = divmod(int(activity.duration.seconds), 60)
                song_length = f'{m1}:{s1}'
                embed.add_field(name="**Duração:**", value=song_length, inline=False)
                await ctx.send(embed=embed)
    else:
        await ctx.send(f'{user.name} não está escutando nada no Spotify')



#   #   # ------------------------------------------ #    #    #




@client.event
async def on_ready():
    print(client.guilds)
    print("fznBOT iniciado com sucesso....")
    print("----------------------------------------------------------------")

    
client.run("")