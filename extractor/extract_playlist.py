import json,boto3
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from config import SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET,SPOTIFY_PLAYLIST_ID,S3_BUCKET,REGION
from utils import utc_timestamp

def get_spotify_client():
    auth=SpotifyClientCredentials(SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET)
    return spotipy.Spotify(auth_manager=auth)

def extract_playlist():
    sp=get_spotify_client()
    results=sp.playlist_items(SPOTIFY_PLAYLIST_ID,additional_types=['track'],limit=100)
    items=results['items']
    while results.get('next'):
        results=sp.next(results)
        items.extend(results['items'])
    return {'playlist_id':SPOTIFY_PLAYLIST_ID,'items':items}

def upload_to_s3(data):
    s3=boto3.client('s3',region_name=REGION)
    key=f"raw/spotify/playlist_id={SPOTIFY_PLAYLIST_ID}/ingest_ts={utc_timestamp()}/payload.json"
    s3.put_object(Bucket=S3_BUCKET,Key=key,Body=json.dumps(data))
    print(f"Uploaded to s3://{S3_BUCKET}/{key}")

if __name__=='__main__':
    data=extract_playlist()
    upload_to_s3(data)
