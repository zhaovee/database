import tkinter as tk
from tkinter import messagebox
import pyodbc

# Database connection
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=DESKTOP-NO3AT26\\SQLEXPRESS;'
                      'DATABASE=Homestay_Order_Database;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# View landlord information and rooms
def view_landlord_info():
    try:
        # Query landlord information
        sql_landlord = "SELECT * FROM Landlord WHERE LandlordID = ?"
        cursor.execute(sql_landlord, (entry_id.get(),))
        landlord = cursor.fetchone()

        if not landlord:
            messagebox.showerror("Error", "Landlord ID does not exist!")
            return

        # Display landlord information
        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END,
                            f"Landlord Information:\nID: {landlord.LandlordID}\nName: {landlord.LandlordName}\nEmail: {landlord.Email}\nPhone Number: {landlord.PhoneNumber}\n\n")

        # Query rooms provided by the landlord
        sql_rooms = "SELECT * FROM Room WHERE LandlordID = ?"
        cursor.execute(sql_rooms, (entry_id.get(),))
        rooms = cursor.fetchall()

        display_area.insert(tk.END, "Provided Rooms:\n")
        for room in rooms:
            display_area.insert(tk.END, f"Room ID: {room.RoomID}, Room No: {room.RoomNo}, Price: {room.Price}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Update landlord information
def update_landlord_info():
    try:
        sql = "UPDATE Landlord SET LandlordName = ?, Email = ?, PhoneNumber = ? WHERE LandlordID = ?"
        cursor.execute(sql, (entry_name.get(), entry_email.get(), entry_phone.get(), entry_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Landlord information updated successfully!")
        view_landlord_info()  # Refresh information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Add a room
def add_room():
    try:
        sql = "INSERT INTO Room (RoomID, LandlordID, RoomNo, Price) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (entry_room_id.get(), entry_id.get(), entry_room_no.get(), entry_price.get()))
        conn.commit()
        messagebox.showinfo("Success", "Room added successfully!")
        view_landlord_info()  # Refresh room information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Delete a room
def delete_room():
    try:
        sql = "DELETE FROM Room WHERE RoomID = ? AND LandlordID = ?"
        cursor.execute(sql, (entry_room_id.get(), entry_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Room deleted successfully!")
        view_landlord_info()  # Refresh room information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Update room information
def update_room_info():
    try:
        sql = "UPDATE Room SET RoomNo = ?, Price = ? WHERE RoomID = ? AND LandlordID = ?"
        cursor.execute(sql, (entry_room_no.get(), entry_price.get(), entry_room_id.get(), entry_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Room information updated successfully!")
        view_landlord_info()  # Refresh room information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# View reservation records
def view_reservations():
    try:
        sql = "SELECT * FROM ReservationRecord WHERE LandlordID = ?"
        cursor.execute(sql, (entry_id.get(),))
        rows = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "Reservation Records:\n")
        for row in rows:
            display_area.insert(tk.END,
                                f"Reservation ID: {row.ReservationID}, Room ID: {row.RoomID}, Guest ID: {row.GuestID}, Date: {row.DateTime}, Payment Status: {row.PayStatus}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# View room income
def view_income():
    try:
        sql = """
        SELECT SUM(Room.Price) AS TotalIncome
        FROM ReservationRecord
        INNER JOIN Room ON ReservationRecord.RoomID = Room.RoomID
        WHERE ReservationRecord.LandlordID = ? AND ReservationRecord.PayStatus = 'Completed';
        """
        cursor.execute(sql, (entry_id.get(),))
        result = cursor.fetchone()

        # Display total income
        display_area.delete('1.0', tk.END)
        total_income = result.TotalIncome if result.TotalIncome else 0  # Return 0 if no records found
        display_area.insert(tk.END, f"Total Income for Landlord {entry_id.get()}: {total_income}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create Tkinter GUI
root = tk.Tk()
root.title("Landlord Management Functions")
root.geometry("1280x720")  # Set window size to 1280x720

# Input fields
tk.Label(root, text="Landlord ID").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Landlord Name").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Email").grid(row=2, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1)

tk.Label(root, text="Phone Number").grid(row=3, column=0)
entry_phone = tk.Entry(root)
entry_phone.grid(row=3, column=1)

tk.Label(root, text="Room ID").grid(row=4, column=0)
entry_room_id = tk.Entry(root)
entry_room_id.grid(row=4, column=1)

tk.Label(root, text="Room No").grid(row=5, column=0)
entry_room_no = tk.Entry(root)
entry_room_no.grid(row=5, column=1)

tk.Label(root, text="Price").grid(row=6, column=0)
entry_price = tk.Entry(root)
entry_price.grid(row=6, column=1)

# Buttons
tk.Button(root, text="View Info", command=view_landlord_info).grid(row=7, column=0)
tk.Button(root, text="Update Info", command=update_landlord_info).grid(row=7, column=1)
tk.Button(root, text="Add Room", command=add_room).grid(row=8, column=0)
tk.Button(root, text="Delete Room", command=delete_room).grid(row=8, column=1)
tk.Button(root, text="Update Room", command=update_room_info).grid(row=9, column=0)
tk.Button(root, text="View Reservations", command=view_reservations).grid(row=9, column=1)
tk.Button(root, text="View Income", command=view_income).grid(row=10, column=0)

# Display area
display_area = tk.Text(root, height=25, width=100)
display_area.grid(row=11, column=0, columnspan=3)

# Start Tkinter main loop
root.mainloop()
