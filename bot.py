import sqlite3
import requests
import random
import os
import io
import discord
import aiohttp
import math
import time

from dotenv import load_dotenv
from discord.ext import commands
from discord import File

load_dotenv()
TOKEN = os.getenv('TOKEN')

conn = sqlite3.connect('gyazo_bot.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user_tokens (user_id TEXT PRIMARY KEY, token TEXT)''')
conn.commit()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

CACHE_EXPIRY = 60
image_cache = {
    'images': [],
    'last_updated': 0
}

def save_token(user_id, token):
    c.execute("INSERT OR REPLACE INTO user_tokens (user_id, token) VALUES (?, ?)", (user_id, token))
    conn.commit()

def get_token(user_id):
    c.execute("SELECT token FROM user_tokens WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    return result[0] if result else None

@tree.command(name='authorize', description='Authorize the bot with your Gyazo token')
async def authorize(interaction: discord.Interaction, token: str = None):
    if token is None:
        instructions = (
            "To authorize this bot to access your Gyazo images, follow these steps:\n"
            "1. Visit the Gyazo API Documentation: https://gyazo.com/oauth/applications\n"
            "2. Log in if you haven't already.\n"
            "3. Create an Application and generate an access token.\n"
            "4. Copy the token and use `/authorize <token>` to authorize the bot."
        )
        await interaction.response.send_message(instructions, ephemeral=True)
    else:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://api.gyazo.com/api/images', headers=headers)
        
        if response.status_code == 200:
            save_token(str(interaction.user.id), token)
            await interaction.response.send_message("Authorization successful! Your Gyazo token has been saved.", ephemeral=True)
        else:
            await interaction.response.send_message("Authorization failed. Please check your token and try again.", ephemeral=True)

async def fetch_all_images_with_cache(token):
    current_time = time.time()
    
    if current_time - image_cache['last_updated'] < CACHE_EXPIRY:
        print("Using cached images.")
        return image_cache['images']

    print("Fetching new images from Gyazo API...")
    headers = {'Authorization': f'Bearer {token}'}
    all_images = []
    page = 1
    per_page = 20

    while True:
        params = {'page': page, 'per_page': per_page}
        response = requests.get('https://api.gyazo.com/api/images', headers=headers, params=params)

        if response.status_code != 200:
            break

        images = response.json()

        if not images:
            break

        all_images.extend(images)
        page += 1
        
    image_cache['images'] = all_images
    image_cache['last_updated'] = current_time

    return all_images

@tree.command(name='lastimages', description='Fetch the most recent images from Gyazo and send them as attachments')
async def lastimages(interaction: discord.Interaction, count: int = 1):
    MAX_IMAGES = 10
    user_id = str(interaction.user.id)
    token = get_token(user_id)

    if not token:
        await interaction.response.send_message("You haven't authorized the bot yet. Use the `/authorize <your_token>` command first.", ephemeral=True)
        return

    if count < 1:
        await interaction.response.send_message("Please specify a number of images greater than 0.")
        return

    count = min(count, MAX_IMAGES)
    await interaction.response.defer()

    images = await fetch_all_images_with_cache(token)

    if images:
        files = []
        async with aiohttp.ClientSession() as session:
            for image in images[:count]:
                img_url = image.get('url') or image.get('thumb_url')

                if img_url:
                    async with session.get(img_url) as img_response:
                        if img_response.status == 200:
                            data = await img_response.read()
                            file_name = img_url.split("/")[-1]
                            files.append(discord.File(io.BytesIO(data), filename=file_name))

        if files:
            await interaction.followup.send(f"Here are your {len(files)} images:", files=files)
        else:
            await interaction.followup.send("No valid images to send.")
    else:
        await interaction.followup.send("No images found.")

@tree.command(name='randomimage', description='Fetch a random image from Gyazo and send it as an attachment')
async def randomimage(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    token = get_token(user_id)

    if not token:
        await interaction.response.send_message("You haven't authorized the bot yet. Use the `/authorize <your_token>` command first.", ephemeral=True)
        return

    await interaction.response.defer()

    all_images = await fetch_all_images_with_cache(token)

    if all_images:
        random_image = random.choice(all_images)
        img_url = random_image.get('url') or random_image.get('thumb_url')

        if img_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(img_url) as img_response:
                    if img_response.status == 200:
                        data = await img_response.read()
                        file_name = img_url.split("/")[-1]
                        file = discord.File(io.BytesIO(data), filename=file_name)
                        await interaction.followup.send("Here is a random image from all your uploads:", file=file)
                    else:
                        await interaction.followup.send("Failed to download the image.")
        else:
            await interaction.followup.send("No valid image URL found.")
    else:
        await interaction.followup.send("No images found.")

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await tree.sync()

client.run(TOKEN)
