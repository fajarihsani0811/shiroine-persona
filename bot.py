import os
import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv

# Memuat token dari file .env
load_dotenv()
DISCORD_TOKEN = os.getenv("MTU2ODU1MjEyMzc3MDA4MTMyMA.GoXqyd.-C8aFxZr_J_mlPKlqYOcerrr2kzxg_jsdYJiUw")

# Mengatur intents bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot berhasil login sebagai {bot.user}")

@bot.command(name="ghrepo")
async def github_repo(ctx, repo_full_name: str):
    """Melihat info repositori GitHub. Contoh: !ghrepo torvalds/linux"""
    url = f"https://api.github.com/repos/{repo_full_name}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                embed = discord.Embed(
                    title=data["full_name"],
                    url=data["html_url"],
                    description=data["description"] or "Tidak ada deskripsi.",
                    color=discord.Color.dark_theme()
                )
                embed.set_thumbnail(url=data["owner"]["avatar_url"])
                embed.add_field(name="⭐ Stars", value=str(data["stargazers_count"]), inline=True)
                embed.add_field(name="🍴 Forks", value=str(data["forks_count"]), inline=True)
                embed.add_field(name="🐞 Open Issues", value=str(data["open_issues_count"]), inline=True)
                embed.add_field(name="💻 Bahasa Utama", value=data["language"] or "Tidak diketahui", inline=True)
                
                await ctx.send(embed=embed)
            elif response.status == 404:
                await ctx.send("❌ Repositori tidak ditemukan! Pastikan formatnya `username/nama-repo`.")
            else:
                await ctx.send(f"⚠️ Terjadi kesalahan saat menghubungi GitHub (Status: {response.status}).")

@bot.command(name="ghuser")
async def github_user(ctx, username: str):
    """Melihat profil pengguna GitHub. Contoh: !ghuser octocat"""
    url = f"https://api.github.com/users/{username}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                embed = discord.Embed(
                    title=data["name"] or data["login"],
                    url=data["html_url"],
                    description=data["bio"] or "Tidak ada bio.",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=data["avatar_url"])
                embed.add_field(name="📦 Public Repos", value=str(data["public_repos"]), inline=True)
                embed.add_field(name="👥 Followers", value=str(data["followers"]), inline=True)
                embed.add_field(name="👣 Following", value=str(data["following"]), inline=True)
                
                await ctx.send(embed=embed)
            elif response.status == 404:
                await ctx.send("❌ Pengguna GitHub tidak ditemukan!")
            else:
                await ctx.send("⚠️ Gagal mengambil data dari GitHub.")

bot.run(MTU2ODU1MjEyMzc3MDA4MTMyMA.GoXqyd.-C8aFxZr_J_mlPKlqYOcerrr2kzxg_jsdYJiUw)
