import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import csv

def save_work_time():
    work_time = work_time_entry.get()
    selected_date = date_entry.get()
    
    # Calculate time allocation based on the percentage
    percentage_allocation = float(percentage_entry.get()) if percentage_entry.get() else 100.0
    default_project_time = round(float(work_time) * (percentage_allocation / 100), 2)
    remaining_time = round(float(work_time) - default_project_time, 2)
    
    selected_project = project_combobox.get()
    other_project = other_project_combobox.get()
    
    if not selected_date or not selected_project:
        return  # Do not proceed if date or project is empty
    
    # Store the work time entries
    work_time_entries.append((selected_date, selected_project, default_project_time))
    
    if remaining_time > 0 and other_project:
        work_time_entries.append((selected_date, other_project, remaining_time))

    # Update the list of saved entries
    update_work_time_list()

def update_work_time_list():
    work_time_list.delete(0, tk.END)
    for i, entry in enumerate(work_time_entries):
        date, project, time = entry
        work_time_list.insert(tk.END, f"Date: {date}, Project: {project}, Work Time: {time} hours")
        # Set a light gray background for alternate rows
        if i % 2 == 1:
            work_time_list.itemconfig(i, {'bg': 'light gray'})

def edit_selected_entry():
    selected_index = work_time_list.curselection()
    if not selected_index:
        return  # No entry selected
    selected_index = selected_index[0]  # Get the first selected index
    selected_entry = work_time_entries[selected_index]
    date_entry.set_date(selected_entry[0])
    project_combobox.set(selected_entry[1])
    work_time_entry.delete(0, tk.END)
    work_time_entry.insert(0, selected_entry[2])

def delete_selected_entry():
    selected_index = work_time_list.curselection()
    if not selected_index:
        return  # No entry selected
    selected_index = selected_index[0]  # Get the first selected index
    work_time_entries.pop(selected_index)
    update_work_time_list()

def export_data():
    with open('work_time_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Project', 'Work Time (hours)'])
        for entry in work_time_entries:
            writer.writerow(entry)

def load_data():
    try:
        with open('work_time_data.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                date, project, time = row
                work_time_entries.append((date, project, float(time)))
        update_work_time_list()
    except FileNotFoundError:
        print("The data file does not exist.")

app = tk.Tk()
app.title("Work Time Tracker")
app.geometry("800x400")

work_time_entries = []

frame = ttk.Frame(app)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

date_label = ttk.Label(frame, text="Select Date:")
date_label.grid(row=0, column=0)

date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
date_entry.grid(row=0, column=1)

project_label = ttk.Label(frame, text="Select Project:")
project_label.grid(row=1, column=0)

# Create a project selection dropdown
project_options = ['Project A', 'Project B', 'Project C', 'Project D']
project_combobox = ttk.Combobox(frame, values=project_options)
project_combobox.grid(row=1, column=1)

other_project_label = ttk.Label(frame, text="Other Project (optional):")
other_project_label.grid(row=2, column=0)

other_project_combobox = ttk.Combobox(frame, values=project_options)
other_project_combobox.grid(row=2, column=1)

percentage_label = ttk.Label(frame, text="Percentage Allocation:")
percentage_label.grid(row=3, column=0)

percentage_entry = ttk.Entry(frame)
percentage_entry.grid(row=3, column=1)

work_time_label = ttk.Label(frame, text="Work Time (hours):")
work_time_label.grid(row=4, column=0)

work_time_entry = ttk.Entry(frame)
work_time_entry.grid(row=4, column=1)

save_button = ttk.Button(frame, text="Save Work Time", command=save_work_time)
save_button.grid(row=5, columnspan=2)

# Create a scrollbar for the Listbox
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.grid(row=6, column=2, rowspan=3, sticky=tk.N + tk.S)

work_time_list = tk.Listbox(frame, height=10, width=100, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
work_time_list.grid(row=6, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)

edit_button = ttk.Button(frame, text="Edit Entry", command=edit_selected_entry)
edit_button.grid(row=9, column=0)

delete_button = ttk.Button(frame, text="Delete Entry", command=delete_selected_entry)
delete_button.grid(row=9, column=1)

export_button = ttk.Button(frame, text="Export Data", command=export_data)
export_button.grid(row=10, columnspan=2)

load_button = ttk.Button(frame, text="Load Data", command=load_data)
load_button.grid(row=11, columnspan=2)

# Configure the scrollbar to work with the Listbox
scrollbar.config(command=work_time_list.yview)

app.mainloop()
