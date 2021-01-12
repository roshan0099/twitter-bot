import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os


class Spotify :
	def __init__(self):
		#credentials	
		self.CLIENT_ID = os.environ.get('CLIENT_ID')
		self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

		#cnnecting with the spotify api using credentials
		self.sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = self.CLIENT_ID, client_secret = self.CLIENT_SECRET))

	#function that gives out random recommendations
	def	recommendation(self):
		rec = self.sp.recommendations(seed_genres = ['acoustic','edm','hip-hop'] , limit = 5)

		for tracks in rec['tracks'] :
			yield tracks['name']


	#getting the id of the artist
	def getting_id(self,artist) :
		try :
			result = self.sp.search(q= artist, limit = 20, type = 'artist')
			id_artist = result['artists']['items'][0]['id']
			return(id_artist)
		except :
			return("ooops an exception has occured, get back to you soon")	

	#to get the top tracks of the particualr artist/band	
	def getting_top_tracks(self,artist_name):

		try :
			jam =[]
			id_artist = self.getting_id(artist_name)
			top_track = self.sp.artist_top_tracks(artist_id = id_artist)
			for no,album in enumerate(top_track['tracks']) :
				if no > 5:
					break
				jam.append(album['name'])
			return(jam)	 
		except :
			return(["ooops an exception has occured"])	

	#function to get the top albums 		
	def artist_albums(self):
		artist_id = self.getting_id("ariana")
		albums = self.sp.artist_albums(artist_id, limit = 4)
		return(albums)

	#function to get the tracks from a particular album
	def getting_tracks_from_album(self,album_id) :
		try :
			album = self.sp.album_tracks(album_id, limit = 10)
			for track in album['items'] :
				yield track['name']
		except :
			return(["oops ....an exception has occured"])		


	def getting_album_id(self,album) :
		try :
			result = self.sp.search(q= album, limit = 20, type = 'album')
			return(result['albums']['items'][0]['id'])
		except :
			return("ooops an exception has occured, get back to you soon")	






