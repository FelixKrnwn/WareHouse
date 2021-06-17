import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image, ImageTk


class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_menu = self.settings.menus[0]
		self.last_current_menu_index = 0
		self.update_mode = False
		self.menus_index = []

		super().__init__(parent) # window.conteiner
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_right_frame()



	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="#d5ddde", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="#d5ddde")
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio),int(i_h/ratio//2)) #(x,y)
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_header, bg="white", width=frame_w, height=frame_h//4)
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14,), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), text="Search", command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.searchbox_frame.grid_columnconfigure(0, weight=3) # 3/4
		self.searchbox_frame.grid_columnconfigure(1, weight=1) # 1/4

	def show_menus_in_listbox(self):
		menus = self.settings.menus
		'''for menu in menus:
			for key, value in menu.items():
				full_name = f"{value['f_name']} {value['l_name']}"
				self.menu_listBox.insert("end", full_name)'''

		for index in self.menus_index:
			menu = menus[index]
			for key, value in menu.items():
				full_name = f"{value['f_name']} {value['l_name']}"
				self.menu_listBox.insert("end", full_name)

	def show_all_menu_in_listbox(self):
		self.menu_listBox.delete(0, 'end')
		menus = self.settings.menus
		self.menus_index = []
		counter_index = 0
		for menu in menus:
			self.menus_index.append(counter_index)
			counter_index += 1
		self.show_menus_in_listbox()

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5

		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.menu_listBox = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.menu_listBox.pack(side="left", fill="both", expand=True)

		self.menus_scroll = tk.Scrollbar(self.left_content)
		self.menus_scroll.pack(side="right", fill="y")

		self.show_all_menu_in_listbox()
		self.menu_listBox.configure(yscrollcommand=self.menus_scroll.set)
		self.menus_scroll.configure(command=self.menu_listBox.yview)

		self.menu_listBox.bind("<<ListboxSelect>>", self.clicked_item_in_Listbox)



	def clicked_item_in_Listbox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				index_item = selection[0]
				
			except IndexError:
				index_item = self.last_current_menu_index

			index = self.menus_index[index_item]
			self.last_current_menu_index = index
			
			print(index_item,"=>", index)

			#value = event.widget.get(index)
			self.current_menu = self.settings.menus[index]
			for menuNumber, info in self.current_menu.items():
				number = menuNumber
				full_name = info['f_name']+" "+info['l_name']
				stock = info['stock']
				price = info['price']

			self.full_name_label.configure(text=full_name)
			self.table_info[0][1].configure(text=number)
			self.table_info[1][1].configure(text=stock)
			self.table_info[2][1].configure(text=price)

	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="#9ad3d6")
		self.right_header.pack()

		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="#9ad3d6")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_menu.values())[0]
		full_name = f"{data['f_name']} {data['l_name']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.full_name_label = tk.Label(self.detail_header, text=full_name, font=("Arial", 30, "bold"), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="#9ad3d6")
		self.full_name_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)




	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="#d5ddde")
		self.right_content.pack(expand=True)

		self.create_detail_right_content()

	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for menuNumber, info, in self.current_menu.items():
			info = [
				['Nomor Menu :', menuNumber],
				['Stock :', info['stock']],
				['Harga :', info['price']]
			]

		self.table_info = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 30), bg="#d5ddde")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)


		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)



	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="#d5ddde")
		self.right_footer.pack()

		self.create_detail_right_footer()
	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 


		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update','Delete', 'Add New']
		commands = [self.clicked_update_button, self.clicked_delete_button, self.clicked_add_new_button]
		self.buttons_features = []

		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="black", fg="#d5ddde", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=(features.index(feature)+1), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def recreate_right_frame(self):

		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()


		self.create_detail_right_header()		
		self.create_detail_right_content()
		self.create_detail_right_footer()

	def recreate_right_frame_after_delete(self):
		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()


		self.create_detail_right_header()		
		self.create_detail_right_content()
		self.create_detail_right_footer()

	def recreate_right_frame_after_add_new(self):
		self.detail_add_header.destroy()
		self.detail_add_content.destroy()
		self.detail_add_footer.destroy()


		self.create_detail_right_header()		
		self.create_detail_right_content()
		self.create_detail_right_footer()
	def recreate_right_frame_after_delete(self):
		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()


		self.create_detail_right_header()		
		self.create_detail_right_content()
		self.create_detail_right_footer()

	def recreate_right_frame_after_add_new(self):
		self.detail_add_header.destroy()
		self.detail_add_content.destroy()
		self.detail_add_footer.destroy()


		self.create_detail_right_header()		
		self.create_detail_right_content()
		self.create_detail_right_footer()


	def clicked_update_button(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for menuNumber, info, in self.current_menu.items():
			info = [
				['Nama Depan :', info['f_name']],
				['Nama Belakang :', info['l_name']],
				['Nomor Menu :', menuNumber],
				['Stock :', info['stock']],
				['price :', info['price']]
			]

		self.table_info = []
		self.entry_update_menu_vars = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="#d5ddde")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_update_content, font=("Arial", 12), bg="#d5ddde", textvariable=entry_var)
					entry.insert(0, info[row][column])
					aRow.append(entry)
					self.entry_update_menu_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
					
			self.table_info.append(aRow)


		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save','Cancel']
		commands = [self.clicked_save_btn, self.clicked_cancel_btn]
		self.buttons_features = []

		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="black", fg="#d5ddde", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=(features.index(feature)+1), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)


	def clicked_delete_button(self):
		self.update_mode = True
		#print(self.last_current_menu_index)

		confirm = msg.askyesnocancel('WarehouseApp Delete Confirmation', 'Are you sure to delete this menu?')
		index = self.last_current_menu_index
		if confirm:
			self.settings.menus.pop(index)
			self.settings.save_data_to_json()
			self.last_current_menu_index = 0
			self.current_menu = self.settings.menus[self.last_current_menu_index]


			self.recreate_right_frame_after_delete()
			self.show_all_menu_in_listbox()


		self.update_mode = False


	def clicked_add_new_button(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_add_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_add_header.grid(row=0, column=0, sticky="nsew")

		
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.add_new_label = tk.Label(self.detail_add_header, text="Tambah Menu Baru", font=("Arial", 30,'bold'), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="#9ad3d6")
		self.add_new_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

		self.detail_add_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_add_content.grid(row=0, column=0, sticky="nsew")

		for numberNumber, info, in self.current_menu.items():
			info = [
				['Nama Depan :', None],
				['Nama Belakang :', None],
				['Nomor Menu :', None],
				['Stock :', None],
				['Harga :', None]
			]

		self.table_info = []
		self.entry_update_menu_vars = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				
				if column == 0:
					label = tk.Label(self.detail_add_content, text=info[row][column], font=("Arial", 12), bg="#d5ddde")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_add_content, font=("Arial", 12), bg="#d5ddde", textvariable=entry_var)
					aRow.append(entry)
					self.entry_update_menu_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
					
			self.table_info.append(aRow)


		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_add_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="#d5ddde")
		self.detail_add_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Add','Cancel']
		commands = [self.clicked_add_btn, self.clicked_cancel_add_btn]
		self.buttons_features = []

		for feature in features:
			button = tk.Button(self.detail_add_footer, text=feature, bg="black", fg="#d5ddde", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=(features.index(feature)+1), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	


	def clicked_save_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('WarehouseApp Save Confirmation', 'Are you sure to update this menu?')

		if confirm:
			f_name = self.entry_update_menu_vars[0].get()
			l_name = self.entry_update_menu_vars[1].get()
			number = self.entry_update_menu_vars[2].get()
			stock = self.entry_update_menu_vars[3].get()
			price = self.entry_update_menu_vars[4].get()
			self.settings.menus[self.last_current_menu_index] = {
				number : {
					"f_name" : f_name,
					"l_name" : l_name,
					"stock" : stock,
					"price" : price
				}
			}
			self.settings.save_data_to_json()
		self.current_menu = self.settings.menus[self.last_current_menu_index]

		self.recreate_right_frame()
		self.menu_listBox.delete(0, 'end')
		self.show_menus_in_listbox()

	def clicked_cancel_btn(self):
		self.update_mode = False

		self.recreate_right_frame()

	def clicked_search_btn(self):
		
		item_search = self.entry_search_var.get()
		if item_search:
			menus = self.settings.menus
			self.menus_index = []
			index_counter = 0
			for menu in menus:
				for numberMenu, info in menu.items():
					if item_search in numberMenu:
						print(numberMenu)
						self.menus_index.append(index_counter)
					elif item_search in info['f_name']:
						print(info['f_name'])
						self.menus_index.append(index_counter)
					elif item_search in info['l_name']:
						print(info['l_name'])
						self.menus_index.append(index_counter)
				index_counter += 1
			print(self.menus_index)
			self.menu_listBox.delete(0, 'end')
			self.show_menus_in_listbox()
		else:
			self.show_all_menu_in_listbox()

	def clicked_add_btn(self):
		self.update_mode = False

		confirm = msg.askyesnocancel('WarehouseApp Save Confirmation', 'Are you sure to add this menu?')

		if confirm:
			f_name = self.entry_update_menu_vars[0].get()
			l_name = self.entry_update_menu_vars[1].get()
			number = self.entry_update_menu_vars[2].get()
			stock = self.entry_update_menu_vars[3].get()
			price = self.entry_update_menu_vars[4].get()
			new_menu = {
				number : {
					"f_name" : f_name,
					"l_name" : l_name,
					"stock" : stock,
					"price" : price
				}
			}
			self.settings.menus.append(new_menu)
			self.settings.save_data_to_json()
		index = len(self.settings.menus)-1
		self.last_current_menu_index = index

			
		self.current_menu = self.settings.menus[self.last_current_menu_index]

		self.recreate_right_frame_after_add_new()
		self.menu_listBox.delete(0, 'end')
		self.show_all_menu_in_listbox()

	def clicked_cancel_add_btn(self):
		self.update_mode = False

		self.recreate_right_frame_after_add_new()




