-- SJSU CMPE 138 FALL 2025 TEAM1
-- Sample Data Loading Script

USE gaming_cafe_db;

-- Insert Memberships
INSERT INTO Membership (MembershipType, StartDate, EndDate, Status) VALUES
('Standard', '2024-01-01', '2025-01-01', 'Active'),
('Premium', '2024-06-01', '2025-06-01', 'Active'),
('VIP', '2024-03-15', '2025-03-15', 'Active'),
('Standard', '2023-12-01', '2024-12-01', 'Expired');

-- Insert Employees (passwords are hashed using SHA2)
INSERT INTO Employee (FullName, Role, Email, ShiftStart, ShiftEnd, AccessLevel, PasswordHash) VALUES
('Sarah Johnson', 'Administrator', 'sarah.j@gamingcafe.com', '09:00:00', '17:00:00', 5, SHA2('admin123', 256)),
('Mike Chen', 'Receptionist', 'mike.c@gamingcafe.com', '08:00:00', '16:00:00', 2, SHA2('recept123', 256)),
('Emily Rodriguez', 'Cashier', 'emily.r@gamingcafe.com', '10:00:00', '18:00:00', 2, SHA2('cashier123', 256)),
('David Kim', 'GameManager', 'david.k@gamingcafe.com', '11:00:00', '19:00:00', 3, SHA2('games123', 256)),
('Lisa Wang', 'AccountManager', 'lisa.w@gamingcafe.com', '09:00:00', '17:00:00', 4, SHA2('account123', 256));

-- Insert Games
INSERT INTO GameTitle (Title, Genre, AgeRestriction, MaxSessionTime, Platform, AvailabilityStatus) VALUES
('League of Legends', 'MOBA', 13, 120, 'PC', 'Available'),
('Valorant', 'FPS', 16, 90, 'PC', 'Available'),
('Fortnite', 'Battle Royale', 13, 120, 'Both', 'Available'),
('Minecraft', 'Sandbox', 7, 180, 'Both', 'Available'),
('Grand Theft Auto V', 'Action', 18, 120, 'Both', 'Available'),
('FIFA 24', 'Sports', 3, 60, 'Console', 'Available'),
('Call of Duty: Modern Warfare', 'FPS', 18, 90, 'Both', 'Available'),
('Overwatch 2', 'FPS', 16, 90, 'PC', 'Available'),
('Roblox', 'Sandbox', 7, 120, 'PC', 'Available'),
('Counter-Strike 2', 'FPS', 18, 90, 'PC', 'Maintenance');

-- Insert Promotions
INSERT INTO Promotions (PromoCode, Description, DiscountValue, StartDate, EndDate, IsActive) VALUES
('WELCOME10', 'New member 10% discount', 10.00, '2024-01-01', '2025-12-31', TRUE),
('WEEKEND25', 'Weekend special 25% off', 25.00, '2024-11-01', '2024-11-30', TRUE),
('STUDENT15', 'Student discount', 15.00, '2024-09-01', '2025-06-30', TRUE),
('EXPIRED20', 'Expired promotion', 20.00, '2024-01-01', '2024-06-30', FALSE);

-- Insert User Accounts (including minors with guardians)
INSERT INTO UserAccount (FullName, DateOfBirth, Email, Phone, IsMinor, GuardianID, MembershipID, JoinDate, CreditBalance, AccountStatus, PasswordHash) VALUES
('John Smith', '1995-03-15', 'john.smith@email.com', '408-555-0100', FALSE, NULL, 1, '2024-01-15', 50.00, 'Active', SHA2('user123', 256)),
('Alice Johnson', '1998-07-22', 'alice.j@email.com', '408-555-0101', FALSE, NULL, 2, '2024-02-20', 100.00, 'Active', SHA2('user456', 256)),
('Bob Williams', '2000-11-30', 'bob.w@email.com', '408-555-0102', FALSE, NULL, NULL, '2024-03-10', 25.00, 'Active', SHA2('user789', 256)),
('Carol Davis', '1992-05-18', 'carol.d@email.com', '408-555-0103', FALSE, NULL, 3, '2024-01-05', 150.00, 'Active', SHA2('vipuser', 256)),
('Tom Martinez', '1997-09-25', 'tom.m@email.com', '408-555-0104', FALSE, NULL, NULL, '2024-04-12', 0.00, 'Active', SHA2('newuser', 256));

-- Insert a guardian account and minor accounts
INSERT INTO UserAccount (FullName, DateOfBirth, Email, Phone, IsMinor, GuardianID, MembershipID, JoinDate, CreditBalance, AccountStatus, PasswordHash) VALUES
('Jennifer Brown', '1985-12-10', 'jennifer.b@email.com', '408-555-0105', FALSE, NULL, NULL, '2024-05-01', 75.00, 'Active', SHA2('parent123', 256));

-- Get the GuardianID we just inserted
SET @guardian_id = LAST_INSERT_ID();

-- Insert minor accounts with guardian
INSERT INTO UserAccount (FullName, DateOfBirth, Email, Phone, IsMinor, GuardianID, MembershipID, JoinDate, CreditBalance, AccountStatus, PasswordHash) VALUES
('Tommy Brown', '2012-08-15', 'tommy.b@email.com', '408-555-0106', TRUE, @guardian_id, NULL, '2024-05-01', 20.00, 'Active', SHA2('kid123', 256)),
('Emma Brown', '2010-04-20', 'emma.b@email.com', '408-555-0107', TRUE, @guardian_id, NULL, '2024-05-01', 15.00, 'Active', SHA2('kid456', 256));

-- Insert Stations
INSERT INTO Station (StationType, Location, Status, AssignedUserID) VALUES
('PC', 'Main Floor - Station 1', 'Available', NULL),
('PC', 'Main Floor - Station 2', 'Available', NULL),
('PC', 'Main Floor - Station 3', 'Available', NULL),
('PC', 'Main Floor - Station 4', 'Maintenance', NULL),
('Console', 'Console Area - Station 1', 'Available', NULL),
('Console', 'Console Area - Station 2', 'Available', NULL),
('PC', 'VIP Room - Station 1', 'Available', NULL),
('PC', 'VIP Room - Station 2', 'Available', NULL);

-- Insert Game Sessions (some active, some finished)
INSERT INTO GameSession (UserID, GameID, StationID, StartTime, EndTime, SessionStatus, TotalTimePlayed) VALUES
(1, 1, 1, '2024-11-13 10:00:00', '2024-11-13 12:00:00', 'Finished', 120),
(2, 2, 2, '2024-11-13 14:00:00', NULL, 'Active', 45),
(3, 3, 3, '2024-11-13 15:00:00', NULL, 'Active', 30),
(4, 4, 7, '2024-11-13 11:00:00', '2024-11-13 14:00:00', 'Finished', 180),
(1, 5, 1, '2024-11-12 16:00:00', '2024-11-12 18:00:00', 'Finished', 120),
(5, 6, 5, '2024-11-13 13:00:00', '2024-11-13 14:00:00', 'Finished', 60);

-- Insert Payments
INSERT INTO Payment (UserID, EmployeeID, Amount, PaymentDateTime, PaymentMethod, PromoApplied) VALUES
(1, 3, 45.00, '2024-11-13 12:00:00', 'Credit Card', 1),
(2, 3, 67.50, '2024-11-13 14:00:00', 'Credit Card', 2),
(3, 3, 30.00, '2024-11-13 15:00:00', 'Cash', NULL),
(4, 3, 90.00, '2024-11-13 14:00:00', 'Account Credit', NULL),
(1, 3, 50.00, '2024-11-12 18:00:00', 'Debit Card', NULL),
(5, 3, 25.50, '2024-11-13 14:00:00', 'Credit Card', 3);

-- Verify data was inserted
SELECT 'Memberships:' AS Table_Name, COUNT(*) AS Row_Count FROM Membership
UNION ALL
SELECT 'Employees:', COUNT(*) FROM Employee
UNION ALL
SELECT 'GameTitles:', COUNT(*) FROM GameTitle
UNION ALL
SELECT 'Promotions:', COUNT(*) FROM Promotions
UNION ALL
SELECT 'UserAccounts:', COUNT(*) FROM UserAccount
UNION ALL
SELECT 'Stations:', COUNT(*) FROM Station
UNION ALL
SELECT 'GameSessions:', COUNT(*) FROM GameSession
UNION ALL
SELECT 'Payments:', COUNT(*) FROM Payment;