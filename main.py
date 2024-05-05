import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import yt_dlp
from colorama import Fore

client_id = '' #Paste your Client ID here
client_secret = '' #Paste your Client Secret here
output = '' #Enter your preferred output path here
redirect_uri = 'http://localhost:8888/callback'
playlist_uri = f'spotify:playlist:{input("Playlist URI: ")}'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

def download_audio(url, output_path):
    try:
        if not os.path.exists(output_path):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path,
            }  
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(Fore.WHITE + f"Audio downloaded successfully to {output_path}")
        else:
            print(Fore.CYAN + f"SKIPPING DOWNLOAD | {output_path}")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

def download_playlist(playlist_uri):
    playlist = sp.playlist(playlist_uri)
    playlist_name = playlist['name'] 
    tracks = sp.playlist_items(playlist_uri, fields='items(track(name,artists))')

    if tracks and 'items' in tracks:
        for item in tracks['items']:
            try: 
                track = item['track']
                track_name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                print(Fore.GREEN + f"STARTING SEARCH | Song: {track_name}")
                search_query = f"{track_name} {artists}"
                output_directory = os.path.join(output, playlist_name) 
                output_filename = f"{track_name} - {artists}.mp3"
                output_path = os.path.join(output_directory, output_filename)
                if not os.path.exists(output_path):
                    ydl = yt_dlp.YoutubeDL()
                    result = ydl.extract_info(f"ytsearch:{search_query}", download=False)
                    if 'entries' in result:
                        video = result['entries'][0]
                        url = video['url'] if 'url' in video else video['webpage_url']
                        if not os.path.exists(output_directory):
                            os.makedirs(output_directory)
                        download_audio(url, output_path)
                    else:
                        print(Fore.RED + f"ERROR | Song: {track_name}")
                else:
                    print(Fore.CYAN + f"SKIPPING SEARCH: {track_name}")
            except Exception as e:
                print(Fore.RED + f"ERROR FETCHING SONG | {e}")

download_playlist(playlist_uri)
