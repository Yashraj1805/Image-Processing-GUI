import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    image.save(output_path)

def swap_pixels(image, key=None):
    pixels = list(image.getdata())
    if key:
        random.seed(key)
    random.shuffle(pixels)
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixels)
    return new_image

def reverse_swap_pixels(image, key=None):
    pixels = list(image.getdata())
    if key:
        random.seed(key)
    original_order = list(range(len(pixels)))
    random.shuffle(original_order)
    reversed_pixels = [None] * len(pixels)
    for i, original_index in enumerate(original_order):
        reversed_pixels[original_index] = pixels[i]
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(reversed_pixels)
    return new_image

def modify_pixels(image, operation="add", value=50):
    pixels = list(image.getdata())
    if operation == "add":
        modified_pixels = [(r+value, g+value, b+value) for r, g, b in pixels]
    elif operation == "subtract":
        modified_pixels = [(r-value, g-value, b-value) for r, g, b in pixels]
    elif operation == "multiply":
        modified_pixels = [(r*value, g*value, b*value) for r, g, b in pixels]
    else:
        modified_pixels = pixels
    modified_pixels = [(min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b))) for r, g, b in modified_pixels]
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(modified_pixels)
    return new_image

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
    if file_path:
        global image
        image = load_image(file_path)
        display_image(image)
        status_label.config(text="Image loaded successfully.")

def save_image_button(image_to_save):
    if image_to_save:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            save_image(image_to_save, output_path)
            messagebox.showinfo("Save Image", f"Image saved as {output_path}")
            status_label.config(text="Image saved successfully.")
    else:
        messagebox.showwarning("No Image", "No image to save. Please process an image first.")

def encrypt_image():
    if image:
        global encrypted_image
        encrypted_image = swap_pixels(image, key=42)
        encrypted_image = modify_pixels(encrypted_image, operation="add", value=int(modify_value_slider.get()))
        display_image(encrypted_image)
        status_label.config(text="Image encrypted successfully.")
    else:
        messagebox.showwarning("No Image", "No image to encrypt. Please load an image first.")

def decrypt_image():
    if encrypted_image:
        decrypted_image = reverse_swap_pixels(encrypted_image, key=42)
        decrypted_image = modify_pixels(decrypted_image, operation="subtract", value=int(modify_value_slider.get()))
        display_image(decrypted_image)
        status_label.config(text="Image decrypted successfully.")
    else:
        messagebox.showwarning("No Image", "No image to decrypt. Please encrypt an image first.")

def display_image(img):
    img.thumbnail((300, 300))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img

# GUI setup
root = tk.Tk()
root.title("Image Processing GUI")

image = None
encrypted_image = None
image_to_save = None

def set_image_to_save(img):
    global image_to_save
    image_to_save = img

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

open_button = tk.Button(frame, text="Open Image", command=open_image)
open_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(frame, text="Save Image", command=lambda: save_image_button(image_to_save))
save_button.pack(side=tk.LEFT, padx=5)

encrypt_button = tk.Button(frame, text="Encrypt Image", command=lambda: (encrypt_image(), set_image_to_save(encrypted_image)))
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(frame, text="Decrypt Image", command=lambda: (decrypt_image(), set_image_to_save(encrypted_image)))
decrypt_button.pack(side=tk.LEFT, padx=5)

modify_label = tk.Label(frame, text="Modify Value:")
modify_label.pack(side=tk.LEFT, padx=5)

modify_value_slider = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL)
modify_value_slider.set(50)
modify_value_slider.pack(side=tk.LEFT, padx=5)

image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

status_label = tk.Label(root, text="Welcome! Load an image to start.", fg="blue")
status_label.pack(padx=10, pady=10)

root.mainloop()
