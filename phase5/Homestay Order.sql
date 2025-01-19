CREATE DATABASE Homestay_Order_Database
USE Homestay_Order_Database

CREATE TABLE Administration (
    AdminID VARCHAR(50) PRIMARY KEY,
    AdminName VARCHAR(50) UNIQUE NOT NULL,
    Name VARCHAR(100),
    Email VARCHAR(100),
    PhoneNumber INT
);

CREATE TABLE Landlord (
    LandlordID VARCHAR(50) PRIMARY KEY,
    LandlordName VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    PhoneNumber INT
);

CREATE TABLE Guest (
    GuestID VARCHAR(50) PRIMARY KEY,
    GuestName VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    PhoneNumber INT
);

CREATE TABLE Room (
    RoomID VARCHAR(50) PRIMARY KEY,
    LandlordID VARCHAR(50) REFERENCES Landlord(LandlordID),
    RoomNo INT NOT NULL,
    Price INT NOT NULL
);

CREATE TABLE ReservationRecord (
    ReservationID VARCHAR(50) PRIMARY KEY,
    LandlordID VARCHAR(50) REFERENCES Landlord(LandlordID),
    GuestID VARCHAR(50) REFERENCES Guest(GuestID),
    RoomID VARCHAR(50) REFERENCES Room(RoomID),
    DateTime VARCHAR(50) NOT NULL,
    PayStatus VARCHAR(20) CHECK (PayStatus IN ('Pending', 'Completed'))
);


INSERT INTO Administration (AdminID, AdminName, Name, Email, PhoneNumber)
VALUES ('A001', 'admin01', 'real-name', 'name@gmail.com', 1234567890);

SELECT * FROM Administration

INSERT INTO Landlord 
VALUES ('L001', 'landlord01', 'password123', 'landlord01@gmail.com', 987654321),
('L003', 'landlord03', 'password789', 'landlord03@gmail.com', 765432109),
('L002', 'landlord02', 'password456', 'landlord02@gmail.com', 876543210),
('L004', 'landlord04', 'password147', 'landlord04@gmail.com',147258369);

SELECT * FROM Landlord


INSERT INTO Room 
VALUES ('R001', 'L001', 101, 500),
('R002', 'L001', 102, 600),
('R003', 'L002', 201, 550),
('R004', 'L002', 202, 650),
('R005', 'L003', 301, 700),
('R006', 'L003', 302, 750);

SELECT * FROM Room


INSERT INTO Guest 
VALUES ('G001', 'guest01', 'guestpass1', 'guest01@gmail.com', 123456789),
('G002', 'guest02', 'guestpass2', 'guest02@gmail.com', 987654321),
('G003', 'guest03', 'guestpass3', 'guest03@gmail.com', 876543210),
('G004', 'guest04', 'guestpass4', 'guest04@gmail.com', 987654322);

SELECT * FROM Guest


INSERT INTO ReservationRecord 
VALUES ('RES001', 'L001', 'G001', 'R001', '1-1-2025', 'Completed'),
('RES002', 'L001', 'G002', 'R002','2-1-2025', 'Pending'),
('RES003', 'L002', 'G003', 'R003', '1-1-2025', 'Completed'),
('RES004', 'L002', 'G001', 'R004', '1-1-2025', 'Completed');

SELECT * FROM ReservationRecord


--Administration Queries
UPDATE Administration
SET Email = 'admin01@gmail.com'
WHERE AdminID = 'A001';

DELETE FROM Guest
WHERE GuestID = 'G004';

DELETE FROM Landlord
WHERE LandlordID = 'L004';

SELECT AVG(Price) AS AveragePrice
FROM Room;

SELECT COUNT(*) AS TotalReservations
FROM ReservationRecord;

SELECT COUNT(*) AS TotalRoom
FROM Room;

SELECT Room.RoomID,Room.RoomNo,Room.Price,Landlord.LandlordName,Landlord.Email
FROM Room
INNER JOIN Landlord ON Room.LandlordID = Landlord.LandlordID
WHERE Room.Price > 600;


SELECT * FROM Administration


--landlord Queries
UPDATE Landlord
SET Email = 'newlandlord01@gmail.com', PhoneNumber = 123456789
WHERE LandlordID = 'L001';

INSERT INTO Room (RoomID, LandlordID, RoomNo, Price)
VALUES ('R007', 'L001', 303, 600);

UPDATE Room
SET Price = 550
WHERE RoomID = 'R007';

SELECT * FROM Room
INNER JOIN ReservationRecord ON Room.RoomID = ReservationRecord.RoomID
WHERE Room.LandlordID = 'L001';

SELECT SUM(Room.Price) AS TotalIncome
FROM ReservationRecord
INNER JOIN Room ON ReservationRecord.RoomID = Room.RoomID
WHERE ReservationRecord.LandlordID = 'L001' AND ReservationRecord.PayStatus = 'Completed';

SELECT * FROM Landlord;


--Guest Queries
UPDATE Guest
SET Email = 'newguest01@gmail.com', PhoneNumber = 987654321
WHERE GuestID = 'G001';

INSERT INTO ReservationRecord (ReservationID, LandlordID, GuestID, RoomID, DateTime, PayStatus)
VALUES ('RES005', 'L003', 'G001', 'R005', '2025-01-5', 'Pending');

UPDATE ReservationRecord
SET DateTime = '2025-01-5', PayStatus = 'Completed'
WHERE ReservationID = 'RES005';

DELETE FROM ReservationRecord
WHERE ReservationID = 'RES005';

SELECT * FROM Guest


--Room Queries
SELECT * FROM Room
WHERE Price > 600;

SELECT * FROM Room
WHERE Price < 600;

SELECT * FROM Room


















