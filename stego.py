import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Data Hiding in Images")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")

        self.img_path = ""
        self.secret_msg = ""
        self.password = ""
        
        tk.Label(root, text="Secure Data Hiding in Images", font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
        
        self.canvas = tk.Canvas(root, width=300, height=200, bg="white")
        self.canvas.pack()
        
        tk.Button(root, text="Select Image", command=self.select_image, bg="#1abc9c", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
        tk.Button(root, text="Encrypt Message", command=self.encrypt, bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
        tk.Button(root, text="Decrypt Message", command=self.decrypt, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
        
        self.status = tk.Label(root, text="Status: Waiting", font=("Arial", 10), fg="white", bg="#2c3e50")
        self.status.pack(pady=10)
    
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.img_path = file_path
            img = Image.open(file_path)
            img = img.resize((300, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(150, 100, image=img)
            self.canvas.image = img
            self.status.config(text="Status: Image Selected")
    
    def encrypt(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        self.secret_msg = simpledialog.askstring("Input", "Enter secret message:")
        self.password = simpledialog.askstring("Input", "Enter a passcode:")
        if not self.secret_msg or not self.password:
            messagebox.showerror("Error", "Message and password cannot be empty!")
            return
        
        img = cv2.imread(self.img_path)
        d = {chr(i): i for i in range(256)}
        
        n, m, z = 0, 0, 0
        for char in self.secret_msg:
            img[n, m, z] = d[char]
            n, m, z = n + 1, m + 1, (z + 1) % 3
        
        encrypted_path = "encryptedImage.png"
        cv2.imwrite(encrypted_path, img)
        os.system(f"start {encrypted_path}")
        
        messagebox.showinfo("Success", "Message encrypted and saved as encryptedImage.png!")
        self.status.config(text="Status: Encryption Successful")
    
    def decrypt(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        
        pas = simpledialog.askstring("Input", "Enter passcode for decryption:")
        if pas != self.password:
            messagebox.showerror("Error", "Incorrect passcode!")
            return
        
        img = cv2.imread("encryptedImage.png")
        c = {i: chr(i) for i in range(256)}
        
        message = ""
        n, m, z = 0, 0, 0
        for _ in range(len(self.secret_msg)):
            message += c[img[n, m, z]]
            n, m, z = n + 1, m + 1, (z + 1) % 3
        
        messagebox.showinfo("Decryption Successful", f"Decrypted Message: {message}")
        self.status.config(text="Status: Decryption Successful")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
