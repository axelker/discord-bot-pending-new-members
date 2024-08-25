import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté avec le user: {bot.user}')

@bot.event
async def on_member_join(member):
    pending_role = discord.utils.get(member.guild.roles, name='pending')
    
    if pending_role:
        await member.add_roles(pending_role)
        await member.send("Bienvenue sur le serveur! Veuillez patienter pendant la validation pour afin de communiquer sur le serveur.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def approve(ctx, member: discord.Member):
    pending_role = discord.utils.get(ctx.guild.roles, name='pending')
    if pending_role in member.roles:
        await member.remove_roles(pending_role)
        await member.add_roles('user')
        await ctx.send(f"{member.mention} a rejoint le serveur!")
    else:
        await ctx.send(f"{member.mention} est déja présent sur le serveur.")

# Gérer l'erreur si un utilisateur sans les bonnes permissions essaie d'exécuter la commande
@approve.error
async def approve_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour approuver les membres.")

bot.run(token)
