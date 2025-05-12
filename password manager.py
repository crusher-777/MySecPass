import tkinter as tk
from tkinter import simpledialog, messagebox
import hashlib
import os
import json
from cryptography.fernet import Fernet
import string

# --- Files ---
DATA_FILE = "passwords.json"
KEY_FILE = "key.key"
MASTER_FILE = "master.key"

# --- Master Password Utilities ---
def hash_master_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return hashed.hex(), salt.hex()

def save_master_password(password):
    hashed_pw, salt = hash_master_password(password)
    with open(MASTER_FILE, "w") as f:
        json.dump({"salt": salt, "hash": hashed_pw}, f)

def verify_master_password(password):
    if not os.path.exists(MASTER_FILE):
        return False
    with open(MASTER_FILE, "r") as f:
        data = json.load(f)
    salt = bytes.fromhex(data["salt"])
    hashed_input, _ = hash_master_password(password, salt)
    return hashed_input == data["hash"]

# --- Encryption Utilities ---
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

fernet = None  # Set after master password is authenticated

# --- Password Strength Checking ---
def check_strength(password):
    length = len(password)
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(c in string.punctuation for c in password)

    total_set = 0
    if upper: total_set += len(string.ascii_uppercase)
    if lower: total_set += len(string.ascii_lowercase)
    if digit: total_set += len(string.digits)
    if symbol: total_set += len(string.punctuation)

    strength_score = sum([length >= 8, upper and lower, digit, symbol])
    strength_percentage = (strength_score / 4) * 100

    crack_time_seconds = estimate_crack_time(strength_score, length, total_set)
    return strength_percentage, crack_time_seconds

def estimate_crack_time(score, length, charset_size):
    guesses_per_second = 100_000_000_000
    combinations = charset_size ** length
    if score <= 2:
        crack_time = combinations / (guesses_per_second * 1000)
    else:
        crack_time = combinations / guesses_per_second

    if crack_time < 60:
        return f"{crack_time:.2f} seconds"
    elif crack_time < 3600:
        return f"{crack_time / 60:.2f} minutes"
    elif crack_time < 86400:
        return f"{crack_time / 3600:.2f} hours"
    else:
        return f"{crack_time / 86400:.2f} days"

# --- Save and Search ---
def save_data(website, username, password):
    if not website or not username or not password:
        messagebox.showwarning("Missing Fields", "All fields are required!")
        return

    entry_data = {
        "username": username,
        "password": password
    }

    encrypted_entry = fernet.encrypt(json.dumps(entry_data).encode()).decode()

    new_data = {
        website: encrypted_entry
    }

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    data.update(new_data)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Success", "Credentials saved and encrypted!")

def search_data(website):
    if not website:
        messagebox.showwarning("Input Required", "Enter a website name.")
        return

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No data file found.")
        return

    if website in data:
        encrypted_entry = data[website]
        try:
            decrypted_entry = fernet.decrypt(encrypted_entry.encode()).decode()
            credentials = json.loads(decrypted_entry)
            messagebox.showinfo("Found", f"Username: {credentials['username']}\nPassword: {credentials['password']}")
        except Exception:
            messagebox.showerror("Error", "Failed to decrypt data.")
    else:
        messagebox.showinfo("Not Found", "No credentials found for this website.")

# --- GUI Actions ---
def save_action():
    save_data(entry_website.get(), entry_username.get(), entry_password.get())

def search_action():
    search_data(entry_website.get())

def check_strength_action():
    password = entry_password.get()
    strength_percentage, crack_time = check_strength(password)
    message = f"Password Strength: {strength_percentage:.2f}%\nEstimated Crack Time: {crack_time}"

    if strength_percentage >= 80:
        messagebox.showinfo("Strength", message)
    else:
        messagebox.showwarning("Weak Password", message)

# --- GUI Setup ---
def launch_gui():
    global entry_website, entry_username, entry_password

    root = tk.Tk()
    root.title("Secure Password Manager")

    tk.Label(root, text="Website").grid(row=0, column=0)
    entry_website = tk.Entry(root, width=30)
    entry_website.grid(row=0, column=1)

    tk.Label(root, text="Username").grid(row=1, column=0)
    entry_username = tk.Entry(root, width=30)
    entry_username.grid(row=1, column=1)

    tk.Label(root, text="Password").grid(row=2, column=0)
    entry_password = tk.Entry(root, width=30, show="*")
    entry_password.grid(row=2, column=1)

    tk.Button(root, text="Save", command=save_action).grid(row=3, column=0, pady=10)
    tk.Button(root, text="Search", command=search_action).grid(row=3, column=1)
    tk.Button(root, text="Check Strength", command=check_strength_action).grid(row=4, column=0, columnspan=2)

    root.mainloop()

# --- Master Password Prompt ---
def authenticate_master():
    global fernet

    if not os.path.exists(MASTER_FILE):
        root = tk.Tk()
        root.withdraw()
        while True:
            password = simpledialog.askstring("Set Master Password", "Create a master password:", show="*")
            confirm = simpledialog.askstring("Confirm Password", "Confirm master password:", show="*")
            if not password or password != confirm:
                messagebox.showerror("Mismatch", "Passwords do not match or empty.")
                continue
            save_master_password(password)
            break
        messagebox.showinfo("Set", "Master password created successfully.")
        fernet = Fernet(load_key())
        launch_gui()
    else:
        root = tk.Tk()
        root.withdraw()
        for _ in range(3):
            password = simpledialog.askstring("Enter Master Password", "Master password:", show="*")
            if password and verify_master_password(password):
                fernet = Fernet(load_key())
                launch_gui()
                return
            else:
                messagebox.showerror("Incorrect", "Wrong master password.")
        messagebox.showerror("Denied", "Too many failed attempts.")
        root.destroy()

# --- Run ---
if __name__ == "__main__":
    authenticate_master()
