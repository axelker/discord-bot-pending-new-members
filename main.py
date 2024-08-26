import discord
from discord.ext import commands
import os
from dotenv import load_dotenv 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all() 

bot = commands.Bot(command_prefix="!", intents=intents)
pending_role_name = 'pending'
base_role_name = 'user'


@bot.event
async def on_ready():
    print(f'Bot connecté avec le user: {bot.user}')

#Manage bot error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        missing_perms = ', '.join(error.missing_perms)
        await ctx.send(f"Vous n'avez pas les permissions nécessaires pour exécuter cette commande. Permissions requises : {missing_perms}.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"L'argument requis '{error.param.name}' est manquant pour cette commande.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Un des arguments fournis est invalide ou n'a pas le bon format. Argument attendu : {error}. Veuillez vérifier votre entrée.")
    elif isinstance(error, discord.Forbidden):
        await ctx.send(f"Je n'ai pas les permissions nécessaires pour effectuer cette action. Message :{error}")
    elif isinstance(error, discord.HTTPException):
        await ctx.send(f"Une erreur de communication avec Discord s'est produite : {error}")
    else:
        await ctx.send(f"Une erreur inattendue s'est produite : {error}")

@bot.event
async def on_member_join(member):
    pending_role = discord.utils.get(member.guild.roles, name=pending_role_name)
    
    if pending_role:
        await member.add_roles(pending_role)
        await member.send("Bienvenue sur le serveur! Veuillez patienter pendant la validation pour afin de communiquer sur le serveur.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def approve(ctx, member: discord.Member):
    pending_role = discord.utils.get(ctx.guild.roles, name=pending_role_name)
    base_role = discord.utils.get(ctx.guild.roles, name=base_role_name)

    if not pending_role:
        await ctx.send(f"Le rôle {pending_role_name} n'existe pas.")
        return
    if ctx.guild.me.top_role <= pending_role:
        await ctx.send(f"Mon rôle n'est pas assez élevé pour retirer le rôle en {pending_role_name}.")
        return
    if ctx.guild.me.top_role <= base_role:
        await ctx.send(f"Mon rôle n'est pas assez élevé pour attribuer le {base_role_name}.")
        return
    if pending_role not in member.roles and base_role in member.roles:
        await ctx.send(f"{member.mention} est déja présent sur le serveur avec le role {base_role_name}.")
        return
    if pending_role in member.roles:
        await member.remove_roles(pending_role)
    if base_role not in member.roles:
        await member.add_roles(base_role)

    roles = [role.name for role in member.roles if role.name != "@everyone"]
    if roles:
        await ctx.send(f"{member.mention} est approuvé sur le serveur et possède désormais les roles suivants : {base_role_name}.")
    else:
        await ctx.send(f"{member.mention} est désormais approuvé sur le serveur sans role spécifique.")


# Manage error for user not have the permission
@approve.error
async def approve_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour approuver les membres.")

bot.run(token)
