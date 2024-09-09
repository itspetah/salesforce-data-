import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options

def download_url(url):
    # Using requests to download content (if it's a direct link to the file)
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        filename = url.split("/")[-1]
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        messagebox.showinfo("Success", f"Downloaded: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

def download_using_selenium(url):
    # Using Selenium for more complex interactions
    try:
        edge_options = Options()
        edge_options.use_chromium = True  # This ensures that the Edge browser is used in Chromium mode
        edge_options.add_experimental_option('detach', True)
        driver = webdriver.Edge(service=EdgeService(), options=edge_options)
        driver.get(url)
        
        # Adjust the below line according to the actual download button's identifier
        download_button = driver.find_element(By.XPATH, '//*[contains(text(), "Download")]')
        download_button.click()
        
        messagebox.showinfo("Success", "Download started in the browser.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initiate download: {e}")

def on_button_click():
    url = url_entry.get()
    if url:
        download_using_selenium(url)
    else:
        messagebox.showwarning("Input Error", "Please enter a URL.")

def load_urls():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_excel(file_path)
        urls = df['URL'].tolist()
        url_listbox.delete(0, tk.END)
        for url in urls:
            url_listbox.insert(tk.END, url)

def on_listbox_select(event):
    selected_url = url_listbox.get(url_listbox.curselection())
    url_entry.delete(0, tk.END)
    url_entry.insert(0, selected_url)

# Set up the GUI
root = tk.Tk()
root.title("Salesforce URL Downloader")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

load_button = tk.Button(frame, text="Load URLs", command=load_urls)
load_button.grid(row=0, column=0, padx=5, pady=5)

url_listbox = tk.Listbox(frame)
url_listbox.grid(row=1, column=0, padx=5, pady=5)
url_listbox.bind('<<ListboxSelect>>', on_listbox_select)

url_label = tk.Label(frame, text="Enter URL:")
url_label.grid(row=2, column=0, padx=5, pady=5)

url_entry = tk.Entry(frame, width=50)
url_entry.grid(row=3, column=0, padx=5, pady=5)

download_button = tk.Button(frame, text="Download", command=on_button_click)
download_button.grid(row=4, column=0, padx=5, pady=5)

root.mainloop()
