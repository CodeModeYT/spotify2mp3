import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import yt_dlp
from colorama import Fore
import json
import re


# Open the json file
with open('config.json') as config_file:
    try:
        config = json.load(config_file)
        print("Config loaded successfully:")
        print(config)
    except json.JSONDecodeError as e:
        print("Error loading config.json:", e)

# Function to extract the Playlist ID from the playlist URL
def extract_playlist_id():
    url = input("Playlist URL: ")
    pattern = r"https://open\.spotify\.com/playlist/([a-zA-Z0-9]+)"
    match = re.search(pattern, url)
    return f'spotify:playlist:{match.group(1)}' if match else None

# Load the preset variales from the json file
client_id = config['spotipy']['client_id']
client_secret = config['spotipy']['client_secret']
output = config['settings']['path']
redirect_uri = 'http://localhost:8888/callback'
playlist_uri = extract_playlist_id()

#Set up the Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

# Function to download the audio from the given URL
def download_audio(url, output_path):
    try:
        if not os.path.exists(output_path):
            # Config for the audio download
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path,
            }
            # Download the audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(Fore.WHITE + f"Audio downloaded successfully to {output_path}")
        else:
            # If the file already exists (= the song already got downlaoded once), skip this download
            print(Fore.CYAN + f"SKIPPING DOWNLOAD | {output_path}")
    #Error handling
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")


def download_playlist(playlist_uri):
    #Aquire the needed Playlist information via the Spotify API
    playlist = sp.playlist(playlist_uri)
    playlist_name = playlist['name'] 
    tracks = sp.playlist_items(playlist_uri, fields='items(track(name,artists))')

    if tracks and 'items' in tracks:
        #Loop through each song of the playlist
        for item in tracks['items']:
            try: 
                # Aquire song information
                track = item['track']
                track_name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                print(Fore.GREEN + f"STARTING SEARCH | Song: {track_name}")
                # Search for the song
                search_query = f"{track_name} {artists}"
                # Set filename and directory
                output_directory = os.path.join(output, playlist_name) 
                output_filename = f"{track_name} - {artists}.mp3"
                output_path = os.path.join(output_directory, output_filename)
                # Check whether the file already exists
                if not os.path.exists(output_path):
                    # Start the search on YouTube and download the song
                    ydl = yt_dlp.YoutubeDL()
                    result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                    if 'entries' in result:
                        video = result['entries'][0]
                        url = video['url'] if 'url' in video else video['webpage_url']
                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        download_audio(url, output_path)
                    else:
                        # Error handling
                        print(Fore.RED + f"ERROR | Song: {track_name}")
                else:
                    # If the file alreadey exists (=track is already saved)
                    print(Fore.CYAN + f"SKIPPING SEARCH: {track_name}")
            # Error handling
            except Exception as e:
                print(Fore.RED + f"ERROR FETCHING SONG | {e}")

# Call the function to downlaod the tracks from the given Playlist (URI)
download_playlist(playlist_uri)
