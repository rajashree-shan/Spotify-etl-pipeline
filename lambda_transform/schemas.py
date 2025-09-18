def extract_songs(data):
    yield ['song_id','song_name']
    for item in data['items']:
        track=item['track']
        yield [track['id'],track['name']]

def extract_albums(data):
    yield ['album_id','album_name']
    for item in data['items']:
        album=item['track']['album']
        yield [album['id'],album['name']]

def extract_artists(data):
    yield ['artist_id','artist_name']
    for item in data['items']:
        for artist in item['track']['artists']:
            yield [artist['id'],artist['name']]
