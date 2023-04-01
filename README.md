
# spotify-backup-import: what is about?!

Tool that will backup the following elements of your Spotify account: 
* All your **Saved Music** (all tracks)
* All your **Saved/Created Playlists**
* All your **Followed Artists**
* All your **Followed Shows/Podcasts**

All those elements will be imported into a new Spotify account that you choose.

What will NOT be backup and imported is:
* All your **Followed Users**
* All your **Created Folders**
* All your **Listen Habits** (NO API)

Other feature are available as creating a playlist of all tracks that aren't in any playlist for further categorization.
elements of your Spotify account

There is a little script *tracks_that_arent_in_any_playlist.py* that will add a functionality:
* Create a Playlist in your Spotify account with all your Saved Tracks that aren't in any Playlist you have created or saved. This can be useful if you want to categorize your Saved Music into some Playlist.

All the code is messy, spaghetti code style. But I tested this very thorugh and I always use this to backup my accounts and import to a new one. There are a lot of improvement that can be done, in order to have a better code. But it works like a charm!


# How to use this tool

You should install python3 and some libraries
```
pip3 install json configparser spotipy
```

Then you can clone this project
```
git clone https://github.com/RegH3x/spotify-backup-import.git
```

You will need two Spotify account. The one that you want to backup, and the one whcih you would like to import everything.


## Step 1: get the keys to make the API work for both Spotify accounts: this step should be done for BOTH accounts (backup and import)

1. Enable your Spotify account for APIs: 
```
https://developer.spotify.com/dashboard/applications
```
        
2. Create a new Application from the dashboard

3. Modify the settings of the created application and create a "Redirect URI":
```
Edit Settings -> "Redirect URIs" -> http://localhost:62500
"Name" -> whatever you like
"Description" -> whatever you like
```

4. Get the "Client ID" and the "Client Secret" from the application page
```
Client ID/Application
Show Client Secret
```

5. When you have the two token write them down, we will need them for the step 2
 

## Step 2: configure the tool to use the two Spotify account

1. Enter the Client ID and Secret ID in the **config_bck.cfg** file for the account you want to **backup**
```
[AUTH]
Client_ID = <your_Backup_Account_Client_ID>
Redirect_URI = http://localhost:62500
Secret = <your_Backup_Account_Secret_ID>
```

2. Enter the Client ID and Secret ID in the **config_import.cfg** file for the account you want to **import**
```
[AUTH]
Client_ID = <your_Import_Account_Client_ID>
Redirect_URI = http://localhost:62500
Secret = <your_Import_Account_Secret_ID>
```


## Step 3: start the tool

Now you can start the tool
```
python3 backup_and_import_account.py
```

Follow the console instruction when executing the tool and enjoy your newly created account with all your things of the backup one!

# How to use *tracks_that_arent_in_any_playlist.py*

This functionality work for your current account, so you have to do the thing done in Step 1 and Step 2 only for you current account. The file used is the **config_bck.cfg**, so put everyhting there.
When everything is configured you can simply launch the script
```
python3 tracks_that_arent_in_any_playlist.py
```

This will create a new playlist in your Spotify account named *Tracks_to_Playlists* which by default will be a private playlist.
Everytime you run this script it will delete the playlist and create a new one always name *Tracks_to_Playlists* with the new songs you have saved, removing the one you have categorized.


# TODO

- [] Keep track of time when the track was added to "Saved tracks" and to a playlist
- [] Reorder the code to make it more object oriented
- [] Clean the code and improve readibility and performance abstracting some methods, some code is redundant

