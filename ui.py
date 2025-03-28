import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000"

url = "http://127.0.0.1:8000/execute"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFZHdpbiIsImV4cCI6MTc0MjcyMjc4Mn0.h2QC3p5v5zWDrKfq94K69qPjFyNdj1nFFfpQQHsoH5s"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {"command": "whoami"}

response = requests.post(url, json=data, headers=headers)

 # Check output
print("Raw Response:", response.text) # Debugging step

try:
    result = response.json()
    print(result)
except requests.exceptions.JSONDecodeError:
    print("Error: Invalid JSON response from server")

def execute_command():
    command = command_entry.get()
    token = token_entry.get()

    if not command or not token:
        messagebox.showerror("Error", "Enter both token and command")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/execute", json={"command": command}, headers=headers)

    if response.status_code == 200:
        output_text.set(response.json()["output"])
    else:
        output_text.set(response.json()["detail"])



# UI Setup
root = tk.Tk()
root.title("Secure System Call Interface")

tk.Label(root, text="Token:").grid(row=0, column=0)
token_entry = tk.Entry(root, width=50)
token_entry.grid(row=0, column=1)

tk.Label(root, text="Command:").grid(row=1, column=0)
command_entry = tk.Entry(root, width=50)
command_entry.grid(row=1, column=1)

execute_btn = tk.Button(root, text="Execute", command=execute_command)
execute_btn.grid(row=2, columnspan=2)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, fg="blue")
output_label.grid(row=3, columnspan=2)

root.mainloop()
