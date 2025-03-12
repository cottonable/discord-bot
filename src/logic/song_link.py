import re
import aiohttp
import discord
import urllib.parse
from colorthief import ColorThief
import io
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

PLATFORM_CAPITALIZATIONS = {
    "Youtube": "YouTube",
    "Youtube Music": "YouTube Music",
    "Itunes": "iTunes",
    "Soundcloud": "SoundCloud",
}

URL_PATTERN = r'^(https?:\/\/[^\s<]+[^<.,:;"\')\]\s])'

class SongData:
    def __init__(self, platform_name, song_name, artist_name, url, thumbnail_url, thumbnail_quality):
        self.platform_name = platform_name
        self.song_name = song_name
        self.artist_name = artist_name
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.thumbnail_quality = thumbnail_quality

async def get_song_data(session, url):
    platforms = []
    encoded_url = urllib.parse.quote(url)
    api_url = f"https://api.song.link/v1-alpha.1/links?url={encoded_url}"
    
    async with session.get(api_url) as response:
        if response.status != 200:
            return None, []
            
        data = await response.json()
        links_by_platform = data.get("linksByPlatform", {})
        entities_by_id = data.get("entitiesByUniqueId", {})
        
        for platform, platform_data in links_by_platform.items():
            entity_id = platform_data.get("entityUniqueId")
            if not entity_id or entity_id not in entities_by_id:
                continue
                
            entity = entities_by_id[entity_id]
            platform_name = platform.title()
            if platform_name in PLATFORM_CAPITALIZATIONS:
                platform_name = PLATFORM_CAPITALIZATIONS[platform_name]
                
            thumbnail_quality = None
            if entity.get("thumbnailWidth") and entity.get("thumbnailHeight"):
                thumbnail_quality = entity["thumbnailWidth"] * entity["thumbnailHeight"]
                
            platforms.append(SongData(
                platform_name=platform_name,
                song_name=entity.get("title"),
                artist_name=entity.get("artistName"),
                url=platform_data.get("url"),
                thumbnail_url=entity.get("thumbnailUrl"),
                thumbnail_quality=thumbnail_quality
            ))
    
    return data.get("pageUrl"), platforms

async def create_song_embed(session, url, ephemeral=False):
    page_url, platforms = await get_song_data(session, url)
    
    if not platforms:
        return {"content": "Couldn't find song information for this link.", "ephemeral": ephemeral}
    
    song_counts = {}
    artist_counts = {}
    
    for platform in platforms:
        if platform.song_name:
            song_counts[platform.song_name] = song_counts.get(platform.song_name, 0) + 1
        if platform.artist_name:
            artist_counts[platform.artist_name] = artist_counts.get(platform.artist_name, 0) + 1
    
    song_name = max(song_counts.items(), key=lambda x: x[1])[0] if song_counts else "Unknown"
    artist_name = max(artist_counts.items(), key=lambda x: x[1])[0] if artist_counts else "Unknown"
    
    platforms.sort(key=lambda p: p.thumbnail_quality if p.thumbnail_quality else 0, reverse=True)
    
    thumbnail_bytes = None
    for platform in platforms:
        if platform.thumbnail_url:
            try:
                async with session.get(platform.thumbnail_url) as response:
                    if response.status == 200:
                        thumbnail_bytes = await response.read()
                        if thumbnail_bytes:
                            break
            except:
                continue
    
    embed = discord.Embed(
        title=discord.utils.escape_markdown(song_name),
        url=page_url,
        description=discord.utils.escape_markdown(artist_name)
    )
    
    file = None
    if thumbnail_bytes:
        file = discord.File(io.BytesIO(thumbnail_bytes), filename="thumbnail.png")
        embed.set_thumbnail(url="attachment://thumbnail.png")
        
        try:
            color_thief = ColorThief(io.BytesIO(thumbnail_bytes))
            dominant_color = color_thief.get_color(quality=1)
            embed.color = discord.Color.from_rgb(*dominant_color)
        except:
            embed.color = discord.Color.blurple()
    else:
        embed.color = discord.Color.blurple()
    
    view = discord.ui.View()
    for platform in platforms[:25]:
        button = discord.ui.Button(label=platform.platform_name, url=platform.url)
        view.add_item(button)
    
    return {
        "embed": embed, 
        "file": file, 
        "view": view, 
        "ephemeral": ephemeral
    }

async def search_song(query):
    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    driver.get("https://odesli.co/")
    
    try:
        search_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#search-page-downshift-input"))
        )
        search_input.send_keys(query)
        
        try:
            first_result = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#search-page-downshift-item-0 a"))
            )
            return first_result.get_attribute("href")
        except TimeoutException:
            no_results = driver.find_elements(By.XPATH, "//div contains(text(), 'No results found')]")
            if no_results:
                raise Exception("No search results found.")
            else:
                raise Exception("Error finding search results.")
    finally:
        driver.quit()

async def get_songlink_embed(link, private="false"):
    async with aiohttp.ClientSession() as session:
        if re.match(URL_PATTERN, link):
            return await create_song_embed(session, link, ephemeral=(private.lower() == "true"))
        else:
            try:
                search_url = await search_song(link)
                if search_url:
                    return await create_song_embed(session, search_url, ephemeral=(private.lower() == "true"))
                else:
                    return {"content": "Couldn't find any songs matching your query.", "ephemeral": True}
            except Exception as e:
                return {"content": f"Error searching for song: {str(e)}", "ephemeral": True}