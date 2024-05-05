# Spotify2MP3 Converter

Convert entire Spotify playlists to MP3 audio files at once - **No Spotify Premium required!**

This tool utilizes the Spotify API to fetch playlist tracks and yt_dlp library to download audio from YouTube.

## Setup Instructions

### Spotify API Setup

1. Head over to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Log in or sign up for a Spotify account.
3. Create an app and obtain your **Client ID** and **Client Secret**.
4. Paste them in `main.py` (line 7-8):

    ```python
    client_id = 'YOUR_CLIENT_ID_HERE'
    client_secret = 'YOUR_CLIENT_SECRET_HERE'
    ```

5. Set the **Redirect URI** to `http://localhost:8888/callback` in your app settings.

### Script Setup

1. Clone/download this repository.
2. Navigate to the directory.
3. Install dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

4. Open `main.py`.
5. Adjust the output directory (line 9):

    ```python
    output = 'D:/Your/Path/Here'
    ```


## Usage

1. Run `main.py`:

    ```
    python main.py
    ```

2. Follow terminal instructions to authenticate with Spotify.
3. The script fetches and downloads playlist tracks.
4. MP3 files will be saved in the specified directory.

## Disclaimer

For educational purposes only. May infringe on Spotify and YouTube terms of service.

Use at your own risk. I take no responsibility for misuse or violation of terms.

## Notes

As this script relies on the YouTube Search, the output may be different from your desired sing and the quality may vary.

## Backstory

Why did I make this?
As a longtime Spotify user, I wanted to download my music without paying a premium. Existing solutions often required payment or lacked bulk conversion options. So, I decided to create this tool.
