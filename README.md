# 🚫 Website Blocker (Python)

## 🚀 Introduction

A robust, automated Python script designed to block distracting websites during your specified working hours. By seamlessly modifying the system's hosts file, it redirects unwanted traffic to your local machine—helping you stay focused and productive.

---

## 🧩 Project Structure

| File Name          | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| Website_Blocker.py | Main script that handles time checking and host file updates |
| website_lists.txt  | Configuration file containing websites to block              |

---

## ⚙️ Features

* ⏰ Time-based website blocking
* 🔄 Automatic unblock outside work hours
* 📝 Simple configuration via text file
* 🖥️ Works at system level (hosts file modification)

---

## 🛠️ Getting Started

### 1. Configure Your Block List

Open the website_lists.txt file and add/remove websites:

Example:
facebook.com
youtube.com
instagram.com

---

### 2. Verify Your Operating System

Default configuration is for Windows:

C:\Windows\System32\drivers\etc\hosts

For macOS/Linux, update the file path inside the script:
/etc/hosts

---

## ▶️ How to Run

⚠️ Administrator Privileges Required

Because the script modifies the system hosts file, you must run it with elevated permissions.

Steps:

1. Open Command Prompt / PowerShell

2. Right-click → Run as Administrator

3. Navigate to your project folder:
   cd path\to\your\project\folder

4. Run the script:
   python Website_Blocker.py

💡 Pro Tip:
Use Task Scheduler (Windows) or cron jobs (Linux/macOS) to automate execution in the background.

---

## 🖼️ Screenshots

### Configuration Example

![carbon](https://user-images.githubusercontent.com/121040100/208466977-cc9e44a7-5963-485b-b0e5-26b6bd44c5c7.png)

### Script Example

![carbon (2)](https://user-images.githubusercontent.com/121040100/208469224-341c11ef-0502-44bf-b219-da95585424b6.png)

---

## ✅ Result

| Time              | Behavior               |
| ----------------- | ---------------------- |
| Working Hours     | Websites are blocked ❌ |
| Non-working Hours | Access is restored ✅   |

---

## 📌 Summary

This project helps eliminate distractions by enforcing website restrictions during productive hours—simple, effective, and customizable.
