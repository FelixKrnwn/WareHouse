import json
from json import load, dump

class Settings:

	def __init__(self):

		#App Conf
		self.title = "Warehouse BIG Restaurant"

		#Window Conf
		base = 75
		ratio =(16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]

		self.screen = f"{self.width}x{self.height}"




		self.logo = "img/big.png"
		self.users_path = "users.json"





		self.menus = None
		self.load_data_from_json()

	def load_data_from_json(self):
		with open("menu.json", "r") as file_json:
			self.menus = load(file_json)
	def save_data_to_json(self):
		with open("menu.json", "w") as file_json:
			dump(self.menus, file_json)




		#DUMMY DATA CONTACTS

		

	def load_data(self, path):
		with open(path, "r") as json_data:
			data = json.load(json_data)
		return data


	def login(self, username, password):
		users = self.load_data(self.users_path)
		if username in users:
			if password == users[username]["password"]:
				return True
			else:
				return False
		else:
			return False
