import json,os
from urllib.parse import unquote_plus
from s3_io import read_json_from_s3,write_csv_to_s3
from schemas import extract_songs,extract_albums,extract_artists

S3_BUCKET=os.environ['S3_BUCKET']

def handler(event,context):
    for record in event['Records']:
        key=unquote_plus(record['s3']['object']['key'])
        payload=read_json_from_s3(S3_BUCKET,key)
        playlist_id=payload.get('playlist_id','unknown')
        ingest_ts=key.split('ingest_ts=')[1].split('/')[0]
        write_csv_to_s3(S3_BUCKET,f'curated/spotify/kind=songs/playlist_id={playlist_id}/ingest_ts={ingest_ts}/songs.csv',extract_songs(payload))
        write_csv_to_s3(S3_BUCKET,f'curated/spotify/kind=albums/playlist_id={playlist_id}/ingest_ts={ingest_ts}/albums.csv',extract_albums(payload))
        write_csv_to_s3(S3_BUCKET,f'curated/spotify/kind=artists/playlist_id={playlist_id}/ingest_ts={ingest_ts}/artists.csv',extract_artists(payload))
    return {'status':'ok'}
