import tkinter as tk
from tkinter import messagebox
import pyodbc

# Database connection
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=DESKTOP-NO3AT26\\SQLEXPRESS;'
                      'DATABASE=Homestay_Order_Database;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# View visitor information and reservations
def view_visitor_info():
    try:
        # Query visitor information
        sql_visitor = "SELECT * FROM Guest WHERE GuestID = ?"
        cursor.execute(sql_visitor, (entry_id.get(),))
        visitor = cursor.fetchone()

        if not visitor:
            messagebox.showerror("Error", "Guest ID does not exist!")
            return

        # Display visitor information
        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END,
                            f"Visitor Information:\nID: {visitor.GuestID}\nName: {visitor.GuestName}\nEmail: {visitor.Email}\nPhone Number: {visitor.PhoneNumber}\n\n")

        # Query visitor reservations
        sql_reservations = """
        SELECT ReservationRecord.ReservationID, Room.RoomID, Room.RoomNo, Room.Price, ReservationRecord.DateTime, ReservationRecord.PayStatus
        FROM ReservationRecord
        INNER JOIN Room ON ReservationRecord.RoomID = Room.RoomID
        WHERE ReservationRecord.GuestID = ?
        """
        cursor.execute(sql_reservations, (entry_id.get(),))
        reservations = cursor.fetchall()

        display_area.insert(tk.END, "Reserved Rooms:\n")
        for reservation in reservations:
            display_area.insert(tk.END,
                                f"Reservation ID: {reservation.ReservationID}, Room ID: {reservation.RoomID}, Room No: {reservation.RoomNo}, Price: {reservation.Price}, Date: {reservation.DateTime}, Payment Status: {reservation.PayStatus}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Update visitor information
def update_visitor_info():
    try:
        sql = "UPDATE Guest SET GuestName = ?, Email = ?, PhoneNumber = ? WHERE GuestID = ?"
        cursor.execute(sql, (entry_name.get(), entry_email.get(), entry_phone.get(), entry_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Visitor information updated successfully!")
        view_visitor_info()  # Refresh information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# View all unreserved rooms
def view_unreserved_rooms():
    try:
        sql = """
        SELECT Room.RoomID, Room.RoomNo, Room.Price, Room.LandlordID
        FROM Room
        WHERE Room.RoomID NOT IN (SELECT RoomID FROM ReservationRecord)
        """
        cursor.execute(sql)
        rooms = cursor.fetchall()

        display_area.delete('1.0', tk.END)
        display_area.insert(tk.END, "Unreserved Rooms:\n")
        display_area.insert(tk.END, f"{'Room ID':<10}{'Room No':<10}{'Price':<10}{'Landlord ID':<15}\n")
        display_area.insert(tk.END, "-" * 50 + "\n")
        for room in rooms:
            display_area.insert(tk.END, f"{room.RoomID:<10}{room.RoomNo:<10}{room.Price:<10}{room.LandlordID:<15}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))



# Reserve a room
def reserve_room():
    try:
        sql = "INSERT INTO ReservationRecord (ReservationID, LandlordID, GuestID, RoomID, DateTime, PayStatus) VALUES (?, ?, ?, ?, GETDATE(), 'Pending')"
        reservation_id = f"Res{entry_room_id.get()}"  # Example: Generate reservation ID based on room ID
        landlord_id = entry_landlord_id.get()  # Input landlord ID for the room
        guest_id = entry_id.get()  # Visitor ID
        room_id = entry_room_id.get()  # Room ID to be reserved

        cursor.execute(sql, (reservation_id, landlord_id, guest_id, room_id))
        conn.commit()
        messagebox.showinfo("Success", "Room reserved successfully!")
        view_visitor_info()  # Refresh reservation information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Cancel reservation
def cancel_reservation():
    try:
        sql = "DELETE FROM ReservationRecord WHERE ReservationID = ? AND GuestID = ?"
        cursor.execute(sql, (entry_reservation_id.get(), entry_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Reservation cancelled successfully!")
        view_visitor_info()  # Refresh reservation information
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create Tkinter GUI
root = tk.Tk()
root.title("Visitor Management Functions")
root.geometry("1280x720")

# Input fields
tk.Label(root, text="Guest ID").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Guest Name").grid(row=1, column=0)
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

tk.Label(root, text="Landlord ID").grid(row=5, column=0)
entry_landlord_id = tk.Entry(root)
entry_landlord_id.grid(row=5, column=1)

tk.Label(root, text="Reservation ID").grid(row=6, column=0)
entry_reservation_id = tk.Entry(root)
entry_reservation_id.grid(row=6, column=1)

# Buttons
tk.Button(root, text="View Info", command=view_visitor_info).grid(row=7, column=0)
tk.Button(root, text="Update Info", command=update_visitor_info).grid(row=7, column=1)
tk.Button(root, text="View Unreserved Rooms", command=view_unreserved_rooms).grid(row=8, column=0)
tk.Button(root, text="Reserve Room", command=reserve_room).grid(row=8, column=1)
tk.Button(root, text="Cancel Reservation", command=cancel_reservation).grid(row=9, column=0)

# Display area
display_area = tk.Text(root, height=25, width=100)
display_area.grid(row=10, column=0, columnspan=3)

# Start Tkinter main loop
root.mainloop()
