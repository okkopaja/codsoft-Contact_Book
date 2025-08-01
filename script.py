import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "contacts.db")

# Database
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        conn.commit()

def load_contacts():
    contact_list.delete(0, tk.END)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone FROM contacts")
        for name, phone in cursor.fetchall():
            contact_list.insert(tk.END, f"{name} - {phone}")

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    
    if name and phone:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
            conn.commit()
        load_contacts()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter both name and phone number.")

def delete_contact():
    try:
        selected_index = contact_list.curselection()[0]
        selected_contact = contact_list.get(selected_index)
        name, phone = selected_contact.split(" - ")

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE name = ? AND phone = ?", (name, phone))
            conn.commit()

        load_contacts()
    except IndexError:
        messagebox.showerror("Error", "No contact selected.")

def clear_contacts():
    result = messagebox.askyesno("Confirm", "Are you sure you want to delete all contacts?")
    if result:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts")
            conn.commit()
        load_contacts()

def get_selected_contact(event):
    try:
        selected_index = contact_list.curselection()[0]
        selected_contact = contact_list.get(selected_index)
        name, phone = selected_contact.split(" - ")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        name_entry.insert(tk.END, name)
        phone_entry.insert(tk.END, phone)
    except IndexError:
        pass


root = tk.Tk()
root.title("Contact Book")
root.geometry("400x500")
root.config(bg="#1E1E2F")

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background="#1E1E2F", foreground="#FFFFFF", font=("Segoe UI", 10))
style.configure("TEntry", padding=6, font=("Segoe UI", 10))
style.configure("RoundedButton.TButton",
                background="#5C67F2",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=10,
                relief="flat")
style.map("RoundedButton.TButton", background=[("active", "#4E52DA")])

frame = tk.Frame(root, bg="#2A2A3D", bd=0, padx=20, pady=20)
frame.pack(pady=30, padx=20, fill="both", expand=True)

name_label = ttk.Label(frame, text="Name:")
name_label.pack(anchor="w", pady=(0, 4))
name_entry = ttk.Entry(frame, width=40)
name_entry.pack(pady=(0, 10))

phone_label = ttk.Label(frame, text="Phone:")
phone_label.pack(anchor="w", pady=(0, 4))
phone_entry = ttk.Entry(frame, width=40)
phone_entry.pack(pady=(0, 10))

add_button = ttk.Button(frame, text="Add Contact", command=add_contact, style="RoundedButton.TButton")
add_button.pack(fill="x", pady=(5, 5))

delete_button = ttk.Button(frame, text="Delete Contact", command=delete_contact, style="RoundedButton.TButton")
delete_button.pack(fill="x", pady=(5, 5))

clear_button = ttk.Button(frame, text="Clear Contacts", command=clear_contacts, style="RoundedButton.TButton")
clear_button.pack(fill="x", pady=(5, 10))

contact_list = tk.Listbox(frame, height=10, bg="#252537", fg="#FFFFFF", font=("Segoe UI", 10),
                          selectbackground="#5C67F2", selectforeground="#FFFFFF", bd=0, relief="flat", highlightthickness=0)
contact_list.pack(fill="both", expand=True, pady=(10, 0))

contact_list.bind('<<ListboxSelect>>', get_selected_contact)

setup_database()
load_contacts()

root.mainloop()
