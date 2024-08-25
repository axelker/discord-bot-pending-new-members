import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all() 

bot = commands.Bot(command_prefix="!", intents=intents)
pending_role_name = 'pending'

@bot.event
async def on_ready():
    print(f'Bot connecté avec le user: {bot.user}')

@bot.event
async def on_member_join(member):
    pending_role = discord.utils.get(member.guild.roles, name=pending_role_name)
    
    if pending_role:
        await member.add_roles(pending_role)
        await member.send("Bienvenue sur le serveur! Veuillez patienter pendant la validation pour afin de communiquer sur le serveur.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def approve(ctx, member: discord.Member):
    base_role_name = 'user'
    pending_role = discord.utils.get(ctx.guild.roles, name=pending_role_name)
    if not pending_role:
        await ctx.send(f"Le rôle {pending_role_name} n'existe pas.")
        return
    if pending_role in member.roles:
        await member.remove_roles(pending_role)
        await member.add_roles(base_role_name)
        await ctx.send(f"{member.mention} a rejoint le serveur en tant que {base_role_name}!")
    else:
        await ctx.send(f"{member.mention} est déja présent sur le serveur et ne possède pas le role {pending_role_name}.")

# Manage error for user not have the permission
@approve.error
async def approve_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour approuver les membres.")

bot.run(token)
