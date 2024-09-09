import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from requests_html import HTMLSession

def download_url(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        response.html.render()  # This will render the JavaScript content
        
        # Adjust the selector to match the download button in the Salesforce page
        download_button = response.html.find('a.download-button-selector', first=True)
        if download_button:
            download_link = download_button.attrs['href']
            download_response = session.get(download_link)
            
            filename = download_link.split("/")[-1]
            with open(filename, 'wb') as file:
                file.write(download_response.content)
                
            messagebox.showinfo("Success", f"Downloaded: {filename}")
        else:
            messagebox.showerror("Error", "Download button not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download: {e}")

def on_button_click():
    url = url_entry.get()
    if url:
        download_url(url)
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
