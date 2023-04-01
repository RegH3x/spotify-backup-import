#!/bin/python3

# Examples: https://github.com/plamere/spotipy/blob/master/examples/
import os
import spotipy
import configparser
import json
from urllib.parse import urlparse, parse_qs
from time import sleep
from spotipy.oauth2 import SpotifyOAuth

# Method for cleaning the envinronment when swithcing accounts
def cleaning():
    if os.path.exists(".cache"): os.remove(".cache")
    else: print("\nThe file .cache does not exist")
    input("\n\n!!! Close the browser and delete the cookies!!!\n\nPress any key when you have finished")
    sleep(1)


# Method to print to console the object retrieved from the API endpoint, if you want to take a closer look to the structure
def print_type_data_debug(obj):
    print("[D] DEBUG ON")
    print('[D] Data type:', type(obj))
    print('[D] Methods:', dir(obj))
    if obj is not None:
        print('\n[D][1L] Keys:', obj.keys())
        
        for k in list(obj.keys()): 
            print('\t[D][1L] Data type of "{}":'.format(k), type(obj[k]))
            if isinstance(obj[k], list):
                print('\t\t[D][2L] Data type of "{}":'.format(k), type(obj[k][0]))
                print('\t\t[D][2L] Keys:', obj[k][0].keys())
                for j in list(obj[k][0].keys()): 
                    print('\t\t[D][2L] Data type of "{}":'.format(j), type(obj[k][0][j]))
                    if isinstance(obj[k][0][j], list):
                        print('\t\t\t[D][3L] Data type of "{}":'.format(j), type(obj[k][0][j][0]))
                        print('\t\t\t[D][3L] 3rd level Keys:', obj[k][0][j][0].keys())
            elif isinstance(obj[k], dict):
                print('\t\t[D][2L] Keys:', obj[k].keys())
                for j in list(obj[k].keys()): 
                    print('\t\t[D][2L] Data type of "{}":'.format(j), type(obj[k][j]))
                    if isinstance(obj[k][j], list):
                        print('\t\t\t[D][3L] Data type of "{}":'.format(j), type(obj[k][j][0]))
                        print('\t\t\t[D][3L] 3rd level Keys:', obj[k][j][0].keys())
            
    
    with open('debug.log','w') as hw: 
        json.dump(obj, hw)

    print('[D] Object written in "debug.log"')

    print("[D] DEBUG OFF")


def get_user_playlists(sp):

    # https://developer.spotify.com/documentation/web-api/reference/get-a-list-of-current-users-playlists
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_playlists

    offset = 0
    limit = 50
    playlists_uri = []

    results = sp.current_user_playlists(limit=limit, offset=offset)
    total_playlists = results['total']

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)

        for i, item in enumerate(results['items']):
            print("\t{}".format(item['name']))
            playlists_uri.append((item['name'], item['uri'], item['public'])) 

        if results['next'] is None: break
        else:
            #print("[D] There are other URLs")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"
            
            url_next = parse_qs(urlparse(results['next']).query)
            offset = url_next['offset'][0]
            limit = url_next['limit'][0]
        sleep(0.5)


    return playlists_uri, total_playlists


def get_tracks_from_playlist(sp, playlist):

    # https://developer.spotify.com/documentation/web-api/reference/get-playlists-tracks
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.playlist_items

    offset = 0
    limit = 100
    playlist_id = playlist[1]

    results = sp.playlist_items(playlist_id, limit=limit, offset=offset)

    total_tracks = results['total']

    tracks_list = []

    while True:
        results = sp.playlist_items(playlist_id, limit=limit, offset=offset, additional_types=('track', 'episode'))

        for i, item in enumerate(results['items']):
            tracks_list.append(item['track']['id']) 

        if results['next'] is None: break
        else:
            #print("[D] There are other URLs")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"
                        
            url_next = parse_qs(urlparse(results['next']).query)
            offset = url_next['offset'][0]
            limit = url_next['limit'][0]
        sleep(0.5)

    return tracks_list, total_tracks


def get_user_tracks(sp):

    # https://developer.spotify.com/documentation/web-api/reference/get-users-saved-tracks
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_saved_tracks

    offset = 0
    limit = 50

    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    total_tracks = results['total']

    liked_tracks = []
    liked_tracks_details = []

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)

        for i, item in enumerate(results['items']):
            liked_tracks.append(item['track']['uri'])
            liked_tracks_details.append( (item['track']['uri'], item['track']['artists'][0]['name'], item['track']['name']) )
            

        if results['next'] is None: break
        else:
            #print("[D] There are other URLs")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"
                     
            url_next = parse_qs(urlparse(results['next']).query)
            offset = url_next['offset'][0]
            limit = url_next['limit'][0]
        sleep(0.5)


    return liked_tracks, liked_tracks_details, total_tracks


def get_followed_artists(sp):

    # https://developer.spotify.com/documentation/web-api/reference/get-followed
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_followed_artists

    after = None
    limit = 50

    results = sp.current_user_followed_artists(limit=limit, after=after)
    #print_type_data_debug(results)

    total_artists = results['artists']['total']

    followed_artists_details = []
    followed_artists = []

    while True:
        results = sp.current_user_followed_artists(limit=limit, after=after)
        
        for i, item in enumerate(results['artists']['items']):
            print("\t{} ({})".format(item['name'], item['popularity']))
            followed_artists.append(item['id'])
            followed_artists_details.append((item['uri'], item['name'], item['genres'], item['popularity'], item['followers']['total']))
            

        if results['artists']['next'] is None:
            #print("[D] Non ci sono altre playlist rimaste")
            break
        else:
            #print("[D] Sono presenti altre playlist")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"
            
            url_next = parse_qs(urlparse(results['artists']['next']).query)
            after = url_next['after'][0]
            limit = url_next['limit'][0]
        sleep(0.5)


    return followed_artists, followed_artists_details, total_artists


def get_user_podcasts(sp):

    # https://developer.spotify.com/documentation/web-api/reference/get-users-saved-shows
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_saved_shows

    offset = 0
    limit = 50

    results = sp.current_user_saved_shows(limit=limit, offset=offset)

    total_shows = results['total']

    saved_shows = []

    while True:
        results = sp.current_user_saved_shows(limit=limit, offset=offset)
        #print_type_data_debug(results)

        for i, item in enumerate(results['items']):
            print("\t{}".format(item['show']['name']))
            saved_shows.append(item['show']['uri'])
            

        if results['next'] is None:
            #print("[D] Non ci sono altre playlist rimaste")
            break
        else:
            #print("[D] Sono presenti altre playlist")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"
            
            url_next = parse_qs(urlparse(results['next']).query)
            offset = url_next['offset'][0]
            limit = url_next['limit'][0]
        sleep(0.5)

    return saved_shows, total_shows




def put_user_tracks(sp, liked_tracks):

    # https://developer.spotify.com/documentation/web-api/reference/save-tracks-user
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_saved_tracks_add

    limit = 50

    # Calculate how many loop we should do in order to import all saved tracks
    number_of_liked_tracks = len(liked_tracks)

    if number_of_liked_tracks <= limit:
        sp.current_user_saved_tracks_add(tracks=liked_tracks)
    
    else:

        for_loop = int(number_of_liked_tracks / limit)
        mod = number_of_liked_tracks % limit

        counter = 0
        for i in range(0, for_loop):
            sp.current_user_saved_tracks_add(tracks=liked_tracks[counter:counter+limit])
            counter +=limit
            sleep(0.5)

        if mod != 0: 
            sp.current_user_saved_tracks_add(tracks=liked_tracks[counter:counter+mod])


def create_new_playlists(sp, playlists_uri, user_id):

    # https://developer.spotify.com/documentation/web-api/reference/create-playlist
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.user_playlist_create

    new_playlists_id = {}

    # Create one playlist at the time
    for r in playlists_uri:
        # user_id, playlist_name, playlist_description
        try:
            new_playlist = sp.user_playlist_create(user_id, r[0], "")
            new_playlists_id[new_playlist['name']] = new_playlist['uri']
        except: 
            print("\n[-] Exception raised for playlist: {}".format(str(r[0])))
        sleep(0.5)

    return new_playlists_id


def put_tracks_to_playlists(sp, tracks_playlists, new_playlists_id):

    # https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.playlist_add_items

    limit=100

    for key_tracks_playlist, value_tracks_playlist in tracks_playlists.items():

        # Fetch the dict of the newly created playlist to match the correct name
        for key_new_playlists_id, value_new_playlists_id in new_playlists_id.items():

            # if the name of playlists match we can start to add tracks
            if key_tracks_playlist == key_new_playlists_id:

                playlist_id = value_new_playlists_id

                print("\n\n[*] Adding tracks for playlist: {}".format(key_tracks_playlist))
                
                try:
                    # check number of tracks for the current playlist
                    number_of_tracks = len(value_tracks_playlist)

                    if number_of_tracks <= limit:
                        sp.playlist_add_items(playlist_id, value_tracks_playlist)
                        sleep(0.5)

                    else:    
                        for_loop = int(number_of_tracks / limit)
                        mod = number_of_tracks % limit
                        
                        counter = 0
                        for i in range(0, for_loop):
                            sp.playlist_add_items(playlist_id, value_tracks_playlist[counter:counter+limit])
                            counter +=limit
                            sleep(0.5)

                        if mod != 0: 
                            sp.playlist_add_items(playlist_id, value_tracks_playlist[counter:counter+mod])

                except: 
                    print("[-] Exception raised for playlist id: {}".format(str(playlist_id)))


def put_user_artists(sp, followed_artists):

    # https://developer.spotify.com/documentation/web-api/reference/follow-artists-users
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.user_follow_artists

    limit = 50

    # Calculate how many loop we should do in order to import all saved tracks
    number_of_followed_artists = len(followed_artists)

    if number_of_followed_artists <= limit:
        sp.user_follow_artists(ids=followed_artists)
    
    else:
        for_loop = int(number_of_followed_artists / limit)
        mod = number_of_followed_artists % limit

        counter = 0
        for i in range(0, for_loop):
            sp.user_follow_artists(ids=followed_artists[counter:counter+limit])
            counter +=limit
            sleep(0.5)

        if mod != 0: 
            sp.user_follow_artists(ids=followed_artists[counter:counter+mod])


def put_user_podcasts(sp, saved_shows):

    # https://developer.spotify.com/documentation/web-api/reference/save-shows-user
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_saved_shows_add

    limit = 50

    # Calculate how many loop we should do in order to import all saved tracks
    number_of_followed_podcasts = len(saved_shows)

    if number_of_followed_podcasts <= limit:
        sp.current_user_saved_shows_add(shows=saved_shows)
    
    else:

        for_loop = int(number_of_followed_podcasts / limit)
        mod = number_of_followed_podcasts % limit

        counter = 0
        for i in range(0, for_loop):
            sp.current_user_saved_shows_add(shows=saved_shows[counter:counter+limit])
            counter +=limit
            sleep(0.5)

        if mod != 0: 
            sp.current_user_saved_shows_add(shows=saved_shows[counter:counter+mod])


def main():
    config = configparser.ConfigParser()
    config.read('config_bck.cfg')

    # Configure all scopes [https://developer.spotify.com/documentation/web-api/concepts/scopes]
    scopes = 'ugc-image-upload playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read user-read-playback-position user-read-recently-played user-top-read app-remote-control streaming user-follow-modify user-follow-read'

    # Cleaning operations
    cleaning()
    
    print("\n\n[*] Connect to the account you want to make the backup...")
    
    # Authentication of backup account
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['AUTH']['Client_ID'],
                                                   client_secret=config['AUTH']['Secret'],
                                                    redirect_uri=config['AUTH']['Redirect_URI'],
                                                    scope=scopes))


    ### 1. BACKUP ALL PLAYLISTS

    # Get all Playlists
    print("\n\n[*] Retrieving all Playlists...")
    
    playlists_uri, total_playlists = get_user_playlists(sp)

    print("\n\n[*] Total Playlist saved: {}\n\n".format(len(playlists_uri)))
    
    # Check the correct number of playlists
    if len(playlists_uri) != total_playlists: print("[-] The number of saved playlists does not match the number of user playlists")


    # Get all Tracks per playlist
    # INPUT: item[0] = name, item[1] = URI, item[2] = public
    # Creation of a dictionary sorted by key, the name of the playlist and the list of associated tracks as a value
    # tracks_playlists["playlist_name"] = list(tracks_id)
    tracks_playlists = {}

    for playlist in playlists_uri:

        playlist_name = playlist[0]
        
        print("\n\t[*] Retrieving all Tracks from Playlist {}".format(playlist_name))
        
        tracks_list, total_tracks_from_playlist = get_tracks_from_playlist(sp, playlist)

        tracks_playlists[playlist_name] = tracks_list
        
        print("\n\t[*] Total Tracks for Saved Playlists: {}\n".format(len(tracks_list)))

        # Check the correct number of tracks inside a playlist
        if len(tracks_list) != total_tracks_from_playlist: print("[-] The number of tracks saved does not match the number of tracks in the user's playlist")



    ### 2. BACKUP ALL TRACKS

    # Get all Liked Tracks
    # liked_tracks = (uri, artist_name, track_name)

    print("\n[*] Retrieving all saved tracks")

    liked_tracks, liked_tracks_details, total_tracks = get_user_tracks(sp)

    print("\n[*] Total Saved Tracks: {}".format(len(liked_tracks)))

    # Check the correct number of saved tracks
    if len(liked_tracks) != total_tracks: print("[-] The number of saved tracks does not match the number of user saved tracks")



    ### 3. BACKUP ALL FOLLOWED ARTISTS

    # Get all Followed Artists
    # followed_artists = (uri, artist_name, genres[], popularity, total_followers)
    print("\n\n[*] Retrieving all Followed Artists (can take a while, depending how many artists were followed)")

    followed_artists, followed_artists_details, total_artists = get_followed_artists(sp)

    print("\n[*] Total Followed Artists: {}\n".format(len(followed_artists)))

    if len(followed_artists) != total_artists: print("[-] The number of followed artists does not match the number of previously followed artists")


    ### 4. BACKUP ALL SAVED SHOWS/PODCASTS
    print("\n\n[*] Retrieving all Podcasts saved")

    saved_shows, total_shows =  get_user_podcasts(sp)
    
    print("\n[*] Total Followed Podcasts: {}\n".format(len(saved_shows)))

    if len(saved_shows) != total_shows: print("[-] The number of podcasts saved does not match the number of podcasts followed by the user")


    # SWITCH ACCOUNTS
        
    # Cleaning operations
    del sp
    cleaning()
    
    config.read('config_import.cfg')
            
    print("\n\n[*] Starting import into new account...")
            
    # Authentication of imported account
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['AUTH']['Client_ID'],
                                                    client_secret=config['AUTH']['Secret'],
                                                    redirect_uri=config['AUTH']['Redirect_URI'],
                                                    scope=scopes))
    
    user_id = sp.me()['id']


    # 1. IMPORT ALL TRACKS

    # Importing all saved tracks
    print("\n\n[*] Importing all Tracks...")
    
    put_user_tracks(sp, liked_tracks)

    print("\n[*] Checking that all tracks are being saved")

    results = sp.current_user_saved_tracks(limit=1, offset=0)
    total_tracks_new = results['total']
    
    if total_tracks_new != total_tracks: print("[-] The number of tracks saved do not match the number of the backup")
    else: print("\n\t[+] Total tracks saved: {}\n".format(total_tracks_new))


    # 2. IMPORT ALL PLAYLISTS

    # Create all Playlists
    print("\n\n[*] Importing all Playlists...")

    results = sp.current_user_playlists(limit=1, offset=0)
    total_playlists_new = results['total']

    # new_playlists_id = {"name_playlist": "URI_playlist", ..}
    if total_playlists_new == 0:
        print("\n\n[*] No playlists found on new account. We can start creating them")
        new_playlists_id = create_new_playlists(sp, playlists_uri, user_id)

    elif total_playlists_new == total_playlists:
        print("\n\n[*] The number of playlists created match the number of the backup. We don't need to create them, we can skip to add tracks to them")
    else:
        print("\n\n[*] Some playlist were created, but them do not match the number of playlists created in the backup. So we will create them")
        new_playlists_id = create_new_playlists(sp, playlists_uri, user_id)
    

    print("\n\n[*] Start Adding tracks or episodes for each playlists created...")
    
    put_tracks_to_playlists(sp, tracks_playlists, new_playlists_id)

    print("\n\n[*] Tracks added to playlists")

        
    # 3. IMPORT ALL ARTISTS
    print("\n\n[*] Importing all Artists...")

    put_user_artists(sp, followed_artists)

    results = sp.current_user_followed_artists(limit=50, after=None)
    total_artists_new = results['artists']['total']


    if total_artists != total_artists_new:
        print("\n\n[-] The number of artists saved do not match the number of the backup")
        print("\n\t[-] Total artists new: {}\n".format(total_artists_new))
        print("\n\t[-] Total artists: {}\n".format(total_artists))
        print("\n\n[-] Maybe a bug in the API as the artist are actually followed")
    else: 
        print("\n\t[+] Total artists saved: {}\n".format(total_artists_new))


    # 4. IMPORT ALL SHOWS/POCASTS
    print("\n\n[*] Importing all Podcasts...")

    put_user_podcasts(sp, saved_shows)

    results = sp.current_user_saved_shows(limit=1, offset=0)

    total_shows_new = results['total']


    if total_shows != total_shows_new:
        print("\n\n[-] The number of podcasts saved do not match the number of the backup")
    else:
        print("\n\t[+] Total podcasts saved: {}".format(total_shows_new))


    print("\n\n[+] Import completed!\n\n")



if __name__ == "__main__": main()
