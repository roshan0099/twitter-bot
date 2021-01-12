import json
import random

class Human :
	def response_text(self,text):
		with open('info.json') as fs :
			data = json.load(fs)
		for no,response in enumerate(data['texts']) :
			for que in response['pattern']:
				if que in text :	
					return data['texts'][no]['response'][random.randint(0,3)]
					break	

		return data['texts'][2]['response'][random.randint(0,2)]


