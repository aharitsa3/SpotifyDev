import sys
import spotipy
import spotipy.util as util
from datetime import date

# spotipy documentation: https://spotipy.readthedocs.io/en/2.12.0/#features


class Music():
    def __init__(self,username,client_id,client_secret,redirect_uri,num_songs=False):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.num_songs = num_songs

        scope = 'user-library-read playlist-modify-public'


        token = util.prompt_for_user_token(self.username, scope, 
                                            client_id=self.client_id,
                                            client_secret=self.client_secret,
                                            redirect_uri=self.redirect_uri)


        if token:
            self.token=True
            self.sp = spotipy.Spotify(auth=token)
        else:
            self.token=False
            print("Can't get token for", self.username)



        today = date.today()
        self.new_playlist_name = "Python {}".format(today)
    

    def make_python_playlist(self,new_playlist_name = False):
        if self.token:
            if new_playlist_name:
                self.new_playlist_name = new_playlist_name
            self.new_playlist_id = 0

            self.generate_python_playlist()

            self.find_recommended_tracks()

            self.replace_songs()

  
        else:
            print("Can't get token for", self.username)


    def generate_python_playlist(self):
        # get user playlist names
        self.user_playlists = self.sp.user_playlists(self.username)
        self.play_lists = []
        for item in self.user_playlists['items']:
            if item['name']==self.new_playlist_name:
                # get playlist ID of "Python"
                self.new_playlist_id = item['id']


        if self.new_playlist_id==0:
            self.sp.user_playlist_create(user=self.username,name=self.new_playlist_name,description="A playlist created by my personal Python script")
            # create playlist if necessary
            print('Created playlist {}'.format(self.new_playlist_name))
            self.user_playlists = self.sp.user_playlists(self.username)
            for item in self.user_playlists['items']:
                if item['name']==self.new_playlist_name:
                    self.new_playlist_id = item['id']


    def find_recommended_tracks(self):
        # Charts Top-100 URI
        self.playlist_id = 'spotify:playlist:37i9dQZEVXbLRQDuF5jeBp'
        self.top_songs_api = self.sp.playlist_tracks(self.playlist_id)

        self.tracks_list = []

        # iterate through current top-N songs
        if not self.num_songs:
            self.num_songs = 10
        self.song_limit = (100//self.num_songs) - 1
        for top_song in self.top_songs_api['items'][:self.num_songs]:
            song_id = top_song['track']['id']
            self.tracks_list.append(song_id)

            # get recommendations
            recommendation_api = self.sp.recommendations(seed_tracks=[song_id],limit=100)
            
            # initialize counter and pointer
            counter = 0
            pointer = 0

            # make sure do not add duplicates
            while counter < self.song_limit:
                song = recommendation_api['tracks'][pointer]
                if song['id'] not in self.tracks_list:
                    self.tracks_list.append(song['id'])
                    counter += 1
                pointer+=1


    def replace_songs(self):
        # add songs to playlist
        self.sp.user_playlist_replace_tracks(self.username,self.new_playlist_id,self.tracks_list)
        print('Successfully added new songs to {} playlist'.format(self.new_playlist_name))



if __name__ == "__main__":
    # read inputted username
    if len(sys.argv) > 1:
        username = sys.argv[1]
        client_id = sys.argv[2]
        client_secret = sys.argv[3]
        redirect_uri = sys.argv[4]
    else:
        # default username
        username = 'aharitsa'
        # my Spotify credentials
        client_id = '8fc52cbddce94b86a6e9a9ed0fb54671'
        client_secret = 'f3dee48642284b3cbd6286a36c659a16'
        redirect_uri = 'http://localhost:8888'
    


    # make Music object
    music = Music(username,client_id,client_secret,redirect_uri)
        

    # generate new playlist
    music.make_python_playlist()