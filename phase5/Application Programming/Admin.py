import tkinter as tk
from tkinter import messagebox
import pyodbc

# Database connection
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=DESKTOP-NO3AT26\\SQLEXPRESS;'
                      'DATABASE=Homestay_Order_Database;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# View administrator information
def view_admin_info():
    try:
        sql = "SELECT * FROM Administration WHERE AdminID = ?"
        cursor.execute(sql, (entry_admin_id.get(),))
        admin = cursor.fetchone()

        if not admin:
            messagebox.showerror("Error", "Admin ID does not exist!")
            return

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "Administrator Information:\n")
        display_area.insert(tk.END, f"Admin ID: {admin.AdminID}\n")
        display_area.insert(tk.END, f"Admin Name: {admin.AdminName}\n")
        display_area.insert(tk.END, f"Name: {admin.Name}\n")
        display_area.insert(tk.END, f"Email: {admin.Email}\n")
        display_area.insert(tk.END, f"Phone Number: {admin.PhoneNumber}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Update administrator information
def update_admin_info():
    try:
        sql = "UPDATE Administration SET AdminName = ?, Email = ?, PhoneNumber = ? WHERE AdminID = ?"
        cursor.execute(sql, (entry_name.get(), entry_email.get(), entry_phone.get(), entry_admin_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Administrator information updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all landlords
def view_all_landlords():
    try:
        sql = "SELECT * FROM Landlord"
        cursor.execute(sql)
        landlords = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "All Landlords:\n")
        for landlord in landlords:
            display_area.insert(tk.END,
                                f"Landlord ID: {landlord.LandlordID}, Name: {landlord.LandlordName}, Email: {landlord.Email}, Phone: {landlord.PhoneNumber}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all guests
def view_all_guests():
    try:
        sql = "SELECT * FROM Guest"
        cursor.execute(sql)
        guests = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "All Guests:\n")
        for guest in guests:
            display_area.insert(tk.END,
                                f"Guest ID: {guest.GuestID}, Name: {guest.GuestName}, Email: {guest.Email}, Phone: {guest.PhoneNumber}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all reservations
def view_all_reservations():
    try:
        sql = """
        SELECT ReservationID, LandlordID, GuestID, RoomID, DateTime, PayStatus
        FROM ReservationRecord
        """
        cursor.execute(sql)
        reservations = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "All Reservations:\n")
        for reservation in reservations:
            display_area.insert(tk.END,
                                f"Reservation ID: {reservation.ReservationID}, Landlord ID: {reservation.LandlordID}, Guest ID: {reservation.GuestID}, Room ID: {reservation.RoomID}, Date: {reservation.DateTime}, Status: {reservation.PayStatus}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all rooms
def view_all_rooms():
    try:
        sql = "SELECT * FROM Room"
        cursor.execute(sql)
        rooms = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "All Rooms:\n")
        for room in rooms:
            display_area.insert(tk.END,
                                f"Room ID: {room.RoomID}, Landlord ID: {room.LandlordID}, Room No: {room.RoomNo}, Price: {room.Price}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Delete a specified user
def delete_user():
    try:
        user_type = user_type_var.get()
        user_id = entry_user_id.get()

        if user_type == "Landlord":
            sql = "DELETE FROM Landlord WHERE LandlordID = ?"
        elif user_type == "Guest":
            sql = "DELETE FROM Guest WHERE GuestID = ?"
        else:
            messagebox.showerror("Error", "Please select a valid user type!")
            return

        cursor.execute(sql, (user_id,))
        conn.commit()
        messagebox.showinfo("Success", f"{user_type} with ID {user_id} deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create Tkinter GUI
root = tk.Tk()
root.title("Administrator Management Functions")
root.geometry("1280x720")

# Input fields
tk.Label(root, text="Admin ID").grid(row=0, column=0, padx=10, pady=10)
entry_admin_id = tk.Entry(root)
entry_admin_id.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Admin Name").grid(row=0, column=2, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=3, padx=10, pady=10)

tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Phone Number").grid(row=1, column=2, padx=10, pady=10)
entry_phone = tk.Entry(root)
entry_phone.grid(row=1, column=3, padx=10, pady=10)

tk.Label(root, text="User ID to Delete").grid(row=2, column=0, padx=10, pady=10)
entry_user_id = tk.Entry(root)
entry_user_id.grid(row=2, column=1, padx=10, pady=10)

user_type_var = tk.StringVar()
user_type_var.set("Select User Type")
tk.OptionMenu(root, user_type_var, "Landlord", "Guest").grid(row=2, column=2, padx=10, pady=10)

# Buttons with adjusted layout
tk.Button(root, text="View Info", command=view_admin_info).grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Update Info", command=update_admin_info).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="View All Landlords", command=view_all_landlords).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="View All Guests", command=view_all_guests).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="View All Reservations", command=view_all_reservations).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="View All Rooms", command=view_all_rooms).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Delete User", command=delete_user).grid(row=6, column=0, columnspan=2, pady=20)

# Display area
display_area = tk.Text(root, height=15, width=100)
display_area.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Start Tkinter main loop
root.mainloop()
