import tweepy 
from music_fetch import Spotify
from time import sleep
from name_fetch import Human
import requests
import os

from pytube import YouTube
from PyDictionary import PyDictionary

#creating an instance 
dictionary = PyDictionary()

#function to download yt videos
def yt_download(url) :
	yt = YouTube(url)



#function to extract meaning of a particulear word 
def dict_meaning(word):
	meaning = dictionary.meaning(word)

	if "Verb" in list(meaning.keys()):
		if len(meaning["Verb"]) > 3 :
			return meaning["Verb"][:3]
		else :
			return meaning["Verb"]	

	else :
		print(meaning)
		if len(meaning["Noun"]) > 3 :
			return meaning["Noun"][:3]
		else :
			return meaning["Noun"]	
							
#extrxt synonym from the given word
def dict_synonym(word) :
	synonym = dictionary.synonym(word)

	if len(synonym) > 4 : 
		return synonym[:4]
	else :
		return synonym	

# function to take in last seen id and also to return it 
def last_seen(FILE,id = 0) :
	if id != 0 :
		f = open(FILE,"w")
		f.write(id)
		id_maintainer = id
		print(type(id_maintainer))
	else :
		f = open(FILE,"r")
		return int(f.read())

#function to extract the name of the artist from the sentence 
def extract_name(text,limit,hash_tag):
	#converting it into list
	name =[]
	name_list = text.split()
	
	split = name_list.index(limit)

	for i in range(split +1,len(name_list)):
		name.append(name_list[i])
	name.remove(hash_tag)		
	return(name)

#function to iterate through the generator and extract the recommendations 
def recommendations():
	suggestions = []
	spotify = Spotify()
	tracks = spotify.recommendation()
	for track in tracks :
		suggestions.append(track)

	return suggestions	


#function to fetch tracks from an album
def tracks_from_album(name):
	try : 
		spotify = Spotify()	 
		album_id = spotify.getting_album_id(name)


		#fetching the tracks
		tracks = spotify.getting_tracks_from_album(album_id)
		return tracks
	except :
		return(["oops an exception has occured "])	


#looping through all the mentions and checking the id
def main_core_loop(mention_info,FILE,api,fs) :
	spotify = Spotify()
	for index,info in enumerate(mention_info) :
		tweet = info.full_text.lower()
	
		try :
			if index == 0 :
				last_seen(FILE,info.id_str)

			if "#beta" in  tweet :

				#condition to check if asked is for recommendation or not 
				if "recommendations" in tweet or "recommend" in tweet or "suggest" in tweet :
					recommended_tracks = recommendations()
					api.update_status(status = "I have found these for you 🕵 : "+", ".join(recommended_tracks),in_reply_to_status_id = info.id,auto_populate_reply_metadata=True) 
				
				#if not it assumes what asked for is top ten tracks
				elif "from" in tweet:
					album_name = extract_name(tweet,'from','#beta')
					tracks = tracks_from_album(album_name)
					api.update_status(status = "here are some of em 🕺 : "+", ".join(tracks),in_reply_to_status_id = info.id,auto_populate_reply_metadata=True)
				else :	
					artist = extract_name(tweet,'of','#beta')
				

					tracks = spotify.getting_top_tracks(" ".join(artist))

					api.update_status(status ="Here are the top 5 tracks : "+ ", ".join(tracks),in_reply_to_status_id = info.id,auto_populate_reply_metadata=True) 	
					


			elif "#info" in tweet	:
				
				reply = """hey 🙋‍♂️ \nThe bot works with  
											keywords and hastags. You want recommendations ? use the keyword recommend/suggest/recommendations with
											#beta at the end (dont forget the hash tag 😿) \n\n
											eg : yo, 'recommend'some tracks #beta => remember 'recommend' and '#beta'😏"""

										
				api.update_status(status = reply ,in_reply_to_status_id = info.id,auto_populate_reply_metadata=True)
				

				


			elif "#dict" in tweet :

				if "meaning" in tweet :
					
					word = extract_name(tweet,'of','#dict')
					meanings = dict_meaning(" ".join(word))
					api.update_status(status = f"I think {' '.join(word)} means 🤔  " + ", ".join(meanings),in_reply_to_status_id = info.id,auto_populate_reply_metadata=True) 				
				
				elif "synonym" in tweet or "synonyms" in tweet :
					word = extract_name(tweet,'of','#dict')
					meanings = dict_synonym(" ".join(word))
					api.update_status(status = "These words kinda mean the same thing => " + ", ".join(meanings),in_reply_to_status_id = info.id,auto_populate_reply_metadata=True) 		

			elif "#yt" in tweet :

					if "https://www.youtube.com" in tweet :

						word = tweet.split()
						# extract_vid = Fetch_id()
						# vid_id = extract_vid.fetch(" ".join(word))
						api.update_status(status = f"😓 hope this works  : https://ytdl0099.herokuapp.com/key={word[2][32:]} \n PS : try this on browser 🤖",in_reply_to_status_id = info.id,auto_populate_reply_metadata=True)
			else :
				#to give out random text based on the tweet
				#like hai, whats your name or simple just oops, error or something
				response = Human()
				text = response.response_text(tweet)
				print(text)
				api.update_status(status = text,in_reply_to_status_id = info.id_str,auto_populate_reply_metadata=True) 


			
		except :
			api.update_status(status = "oops an excpetion has occured, will get back to you soon",in_reply_to_status_id = info.id,auto_populate_reply_metadata=True) 
	fs.close()


def main() :

	#all the important keys
	consumer_key =  os.environ.get('CONSUMER_KEY') 
	consumer_secret = os.environ.get('CONSUMER_SECRET')
	access_token = os.environ.get('ACCESS_TOKEN')
	access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

	#assigning the OAuth 
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

	auth.set_access_token(access_token,access_token_secret)

	api = tweepy.API(auth)

	FILE = "id_mentions.txt"

	#opening up a file to append the id key and to read so as to avoid the repeatation 
	fs = open("id_mentions.txt","a")
	fr = open("id_mentions.txt","r")


	#looping the core function and updating the last seen file at the same time 
	while True :
		
		mention_info = api.mentions_timeline(last_seen(FILE),tweet_mode = "extended")
		# print(mention_info)
		# for index,info in enumerate(mention_info) :
		# 	print(info.id_str)
		main_core_loop(mention_info,FILE,api,fs)
		sleep(20)


# text = "@call_meanytime meaning of cut #dict"
# jam = extract_name(text,"of","#dict")


# print(" ".join(jam))

# dirname = os.path.dirname("Procfile")
# print(dirname)
# print("sup")

# sam = text.split()
# print(sam[1][32:])

if __name__ == '__main__':
	main()


 