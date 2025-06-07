# 🔐 Secure Password Manager 

A lightweight, secure password manager for Windows — no installation required. Simply run the application and manage your website credentials securely offline.

---

## ✅ What It Does
This app lets you:
- 🔐 Store usernames & passwords **securely** on your computer
- 🔑 Protect access with a **master password**
- 📈 Analyze password strength and estimate crack time

All stored data is **encrypted**, and the app runs without needing internet or additional setup.

---

## 🖥️ Features
- **Master Password Protection** – your vault is locked with a secure password
- **Local Encryption** – passwords are encrypted using strong cryptography
- **Password Strength Checker** – evaluates password quality and crack resistance
- **Simple Interface** – clean and intuitive GUI 
- **Portable** – just click the application and it will run without any insallation

---

## 📁 Files Created (Automatically)
| File           | Purpose                                   |
|----------------|-------------------------------------------|
| `passwords.json` | Encrypted storage for your credentials     |
| `master.key`     | Contains hashed & salted master password  |
| `key.key`        | Encryption key used to encrypt/decrypt    |

> These files are created in the same directory where the application is run.

---

## 🚀 How to Use
1. **Double-click the application file**
2. Set a **master password** (first-time use)
3. Enter website credentials
4. Save them securely
5. Search or review passwords when needed

You can also use the **Check Strength** button to assess how strong your password is and how long it might take to crack.

---

## 🛡️ Security Notice
- All credentials are stored **locally** and **encrypted**
- Your master password is hashed using a secure algorithm (PBKDF2 + SHA-256 + salt)
- Only you can access the data with your master password
