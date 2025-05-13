# secure-password-manager
this project can store your websites username and passwords offline and also analyze password strength  




# 📚 Secure Password Manager

A simple yet secure password manager built with **Python** and **Tkinter**, using **Fernet encryption** to safely store your credentials.  
All saved data is encrypted and only accessible through a master password.

---

## 🔐 Features

- 🔑 Master password protection (securely hashed and salted)
- 🔐 Encrypted storage of usernames & passwords using `cryptography.fernet`
- 📈 Password strength checker with estimated crack time
- 🖥️ Easy-to-use Tkinter-based GUI
- 💾 Local encrypted storage (`passwords.json`)
- 🧩 Lightweight, standalone Python script

---

## 🖥️ GUI Preview

> The interface provides:
> - Website input  
> - Username input  
> - Password input (masked)  
> - Save, Search, and Check Strength buttons

---

## 📁 Files Created

| File            | Purpose                                |
|------------------|----------------------------------------|
| `passwords.json` | Stores encrypted credentials (not readable) |
| `master.key`     | Stores master password hash & salt     |
| `key.key`        | Symmetric encryption key for Fernet    |

---

## 🛠️ Requirements

- Python 3.7+
- Libraries:
  - `tkinter` (standard in Python)
  - `cryptography`

Install dependencies with:

```bash
pip install -r requirements.txt
