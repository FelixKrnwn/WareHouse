import tkinter as tk
from tkinter import messagebox as msg

from settings import Settings
from appPage import AppPage
from loginPage import LoginPage

class Window(tk.Tk):

	def __init__(self, App):
		self.app = App
		self.settings = App.settings

		super().__init__()
		self.title(self.settings.title)
		self.geometry(self.settings.screen)
		self.resizable(0,0)

		self.create_menu()
		self.create_container()
		
		self.pages = {}
		self.create_appPage()
		self.create_loginPage()

	def change_page(self, page):
		page = self.pages[page]
		page.tkraise()

	def auth_login(self):
		username = self.pages['loginPage'].var_username.get()
		password = self.pages['loginPage'].var_password.get()

		granted = self.settings.login(username, password)
		if granted:
			self.change_page('appPage')

		self.pages['loginPage'].setToEmptyEntry()


	def create_menu(self):
		self.menuBar = tk.Menu(self)
		self.configure(menu=self.menuBar)

		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label="New Menu", command=self.show_new_menu_info)

		self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
		self.helpMenu.add_command(label="About", command=self.show_about_info)

		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)


	def create_container(self):
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)

	def create_appPage(self):
		self.pages["appPage"] = AppPage(self.container, self.app)

	def create_loginPage(self):
		self.pages['loginPage'] = LoginPage(self.container, self)
	

	def show_about_info(self):
		msg.showinfo("About Warehouse App", "This apps created by\n1. Felix\n2. Riccardo\n\nCopyright-2021")
	def show_new_menu_info(self):
		msg.showinfo("Add New Menu", "To Add a menu\nPlease press the Add New Button")

	def exit_program(self):
		msg.askyesnocancel("Exit Program", "Do you sure to exit program?")
		if respond:
			sys.exit()


class WarehouseApp:

	def __init__(self):
		self.settings = Settings()
		self.window = Window(self)

	def run(self):
		self.window.mainloop()

if __name__ == '__main__':
	myWarehouseApp = WarehouseApp()
	myWarehouseApp.run()