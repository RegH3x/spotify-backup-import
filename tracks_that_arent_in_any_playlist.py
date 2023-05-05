#!/bin/python3

# examples: https://github.com/plamere/spotipy/blob/master/examples/
import os
import spotipy
import configparser
import json
from urllib.parse import urlparse, parse_qs
from time import sleep
from spotipy.oauth2 import SpotifyOAuth

def cleaning():
    if os.path.exists(".cache"): os.remove(".cache")
    else: print("\nThe file .cache does not exist")
    input("\n\n!!! Close the browser and delete the cookies!!!\n\nPress any key when you have finished")
    sleep(1)


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


def get_user_playlists(sp, playlist_to_not_touch):

    # https://developer.spotify.com/documentation/web-api/reference/get-a-list-of-current-users-playlists
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.current_user_playlists

    offset = 0
    limit = 50
    playlists_uri = []
    flag = False

    results = sp.current_user_playlists(limit=limit, offset=offset)
    total_playlists = results['total']

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        #print_type_data_debug(results)

        for i, item in enumerate(results['items']):
            print("\t{}".format(item['name']))
            if item['name'] == playlist_to_not_touch:
                flag = True
                id_playlist_to_not_touch = item['uri']
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


    return playlists_uri, total_playlists, flag, id_playlist_to_not_touch


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
    results = True

    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    total_tracks = results['total']

    liked_tracks = []
    
    print("\n\t[+] Getting tracks with offset {}".format(offset))
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)

    while results:


        for i, item in enumerate(results['items']):
            liked_tracks.append(item['track']['id'])
            

        if results['next']:
            #print("[D] There are other URLs")
            # get parameters from URL
            #   "next": "https://api.spotify.com/v1/users/31vux7lk7axk3fmoofhftiypj7bq/playlists?offset=10&limit=10"

            offset = parse_qs(urlparse(results['next']).query)['offset'][0]
            print("\n\t[+] Getting tracks with offset {}".format(offset))

            print(results['next'])
            results = sp.next(results)

        else: 
            results = None

        sleep(0.5)


    return liked_tracks, total_tracks


def put_tracks_to_playlist(sp, tracks_playlists, playlist_id):

    # https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
    # https://spotipy.readthedocs.io/en/2.22.1/?highlight=current_user_playlists#spotipy.client.Spotify.playlist_add_items

    limit=100

    try:
        # check number of tracks for the current playlist
        number_of_tracks = len(tracks_playlists)

        if number_of_tracks <= limit:
            sp.playlist_add_items(playlist_id, tracks_playlists)
        else:    
            for_loop = int(number_of_tracks / limit)
            mod = number_of_tracks % limit
                        
            counter = 0
            for i in range(0, for_loop):
                sp.playlist_add_items(playlist_id, tracks_playlists[counter:counter+limit])
                counter +=limit
                sleep(0.5)

            if mod != 0: 
                sp.playlist_add_items(playlist_id, tracks_playlists[counter:counter+mod])

    except: print("[-] Exception raised for playlist id: {}".format(str(playlist_id)))


def main():
    config = configparser.ConfigParser()
    config.read('config_bck.cfg')

    # Configure all scopes [https://developer.spotify.com/documentation/web-api/concepts/scopes]
    scopes = 'ugc-image-upload playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-modify user-library-read user-read-playback-position user-read-recently-played user-top-read app-remote-control streaming user-follow-modify user-follow-read'

    # Cleaning operations
    cleaning()
    
    print("\n\n[*] Connecting to the account you want to make the backup...")
    
    # Authentication of backup account
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config['AUTH']['Client_ID'],
                                                   client_secret=config['AUTH']['Secret'],
                                                    redirect_uri=config['AUTH']['Redirect_URI'],
                                                    scope=scopes))
    
    user_id = sp.me()['id']

    # Playlist used to add the tracks that aren't in any playlist
    playlist_to_not_touch = 'Tracks_to_Playlists'


    ### 1. BACKUP ALL PLAYLISTS

    # Get all Playlists
    print("\n\n[*] Retrieving all Playlists...")
    
    playlists_uri, total_playlists, flag, id_playlist_to_not_touch = get_user_playlists(sp, playlist_to_not_touch)

    print("\n\n[*] Total Saved Playlists: {}\n\n".format(len(playlists_uri)))

    if len(playlists_uri) != total_playlists: print("[-] The number of saved playlists does not match the number of user playlists")


    # Get all Tracks per playlist
    # INPUT: item[0] = name, item[1] = URI, item[2] = public
    tracks_playlists = []

    for playlist in playlists_uri:

        playlist_name = playlist[0]
        
        if playlist_name != playlist_to_not_touch:

            print("\n\t[*] Retrieving all Tracks from Playlist {}".format(playlist_name))
            
            tracks_list, total_tracks_from_playlist = get_tracks_from_playlist(sp, playlist)

            tracks_playlists.extend(tracks_list)
            
            print("\n\t[*] Total Tracks Saved Playlist: {}\n".format(len(tracks_list)))
            
            
            if len(tracks_list) != total_tracks_from_playlist: print("[-] The number of tracks saved does not match the number of tracks in the user's playlist")



    ### 2. BACKUP ALL TRACKS

    # Get all Liked Tracks
    # liked_tracks = (uri, artist_name, track_name)

    print("\n[*] Retrieving all saved tracks (liked one)")

    liked_tracks, total_tracks = get_user_tracks(sp)

    if len(liked_tracks) != total_tracks: print("[-] The number of saved tracks does not match the number of user saved tracks")


    print("\n\n[*] Total tracks saved: {}".format(len(liked_tracks)))
    print("\n[*] Total tracks in all playlists: {}".format(len(tracks_playlists)))

    # We do the difference between the list of saved tracks and the list of all tracks in playlists
    # saved_tracks - tracks_in_all_playlist = track_that_arent_in_any_playlist
    set_tracks_playlists = set(tracks_playlists)
    tracks_no_playlist = [x for x in liked_tracks if x not in set_tracks_playlists]

    print("\n\n[*] Tracks that will be added to the new playlist: {}\n".format(len(tracks_no_playlist)))    

    # Check that playlist exist, if not create one, if exist delete first
    if flag: 
        print("\n[*] Deleting old playlist")
        # split maybe due bug into spotipy API for this specific method
        sp.current_user_unfollow_playlist(id_playlist_to_not_touch.split(':')[2])
    sleep(5)

    print("\n[*] Creating new playlist")
    playlist_id = sp.user_playlist_create(user_id, playlist_to_not_touch, public=False, description="All tracks that arent in any playlist")
    id_playlist_to_not_touch = playlist_id['uri']

    print("\n[*] Put tracks inside playlist\n")
    put_tracks_to_playlist(sp, tracks_no_playlist, id_playlist_to_not_touch)

    print("\n[+] Now in your spotify account you have a playlist named '{}' which have all tracks that arent in any playlist\n\n".format(playlist_to_not_touch))

    del sp


if __name__ == "__main__": main()
