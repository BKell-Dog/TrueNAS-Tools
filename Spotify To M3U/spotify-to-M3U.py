import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = 'hidden'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'hidden'

# Initialize Spotipy client with Client Credentials flow
credentials = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=credentials)

def fetchTrackNames(playlist_id):
    """Fetch all track names from a Spotify playlist and return them as a list."""
    track_names = []
    limit = 100
    offset = 0

    while True:
        response = sp.playlist_tracks(
            playlist_id,
            offset=offset,
            limit=limit,
            fields='items.track.name,total'
        )
        items = response['items']

        for item in items:
            track_names.append(item['track']['name'])

        offset += len(items)
        if offset >= response['total']:
            break

    return track_names

def create_m3u_files(base_dir):
    # Walk through each folder in the base directory
    for root, dirs, files in os.walk(base_dir):
        # Filter out music files by extensions (add more as needed)
        music_files = [f for f in files if f.lower().endswith(('.mp3', '.wav', '.flac', '.aac'))]

        # Skip folders without music files
        if not music_files:
            continue

        # Create the M3U file in the folder
        playlist_path = os.path.join(root, 'playlist.m3u')
        with open(playlist_path, 'w', encoding='utf-8') as m3u_file:
            for music_file in music_files:
                # Write each music file path relative to the current folder
                m3u_file.write(music_file + '\n')

        print(f"Created playlist: {playlist_path}")

def writeToFile(lines, output_file):
    """Write a list of lines to a text file, one per line."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def savePlaylist(playlist_id):
    """Fetch track names from a playlist and save them to a file."""
    track_names = fetchTrackNames(playlist_id)
    print(track_names)
    print(f"Saved {len(track_names)}")


# Example usage:
if __name__ == '__main__':
    playlist_id = 'https://open.spotify.com/playlist/4nKWAQrtACMK6NqAxI1DWF?si=62755ab2ddfd49e4'
    output_file = 'playlist_tracks.txt'
    savePlaylist(playlist_id)

# Replace 'your/music/library/path' with the path to your music library
# create_m3u_files('your/music/library/path')
