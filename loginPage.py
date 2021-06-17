#loginPage.py
import tkinter as tk
from PIL import Image, ImageTk


class LoginPage(tk.Frame):
	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings

		super().__init__(parent)
		self.configure(bg="black")
		self.grid(row=0, column=0, sticky="nsew")
		parent.grid_columnconfigure(0, weight=1)
		parent.grid_rowconfigure(0, weight=1)

		#CREATE MAIN FRAME
		self.main_frame = tk.Frame(self, height=self.settings.height, width=self.settings.width, bg="black")
		self.main_frame.pack(expand=True)

		image = Image.open(self.settings.logo)
		image_w, image_h = image.size
		ratio = image_w/self.settings.width
		image = image.resize((int(image_w//ratio//6),int(image_h//ratio//6)))

		self.logo = ImageTk.PhotoImage(image)
		self.label_logo = tk.Label(self.main_frame, image=self.logo)
		self.label_logo.pack(pady=5)

		self.label_username = tk.Label(self.main_frame, text="Username : ", font=("Arial", 18, "bold"), bg="black", fg="white")
		self.label_username.pack(pady=5)

		self.var_username = tk.StringVar()
		self.entry_username = tk.Entry(self.main_frame, font=("Arial", 16, "bold"), textvariable=self.var_username)
		self.entry_username.pack(pady=5)

		self.label_password = tk.Label(self.main_frame, text="Password : ", font=("Arial", 18, "bold"), bg="black", fg="white")
		self.label_password.pack(pady=5)

		self.var_password = tk.StringVar()
		self.entry_password = tk.Entry(self.main_frame, font=("Arial", 16, "bold"), show="*", textvariable=self.var_password)
		self.entry_password.pack(pady=5)

		self.btn_login = tk.Button(self.main_frame, text="LOGIN", font=("Arial", 18, "bold"), command=lambda:self.app.auth_login())
		self.btn_login.pack(pady=5)

	def setToEmptyEntry(self):
		self.var_username.set("")
		self.entry_username.configure(textvariable = self.var_username)

		self.var_password.set("")
		self.entry_password.configure(textvariable = self.var_password)
