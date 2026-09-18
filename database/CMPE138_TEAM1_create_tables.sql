-- SJSU CMPE 138 FALL 2025 TEAM1
-- Gaming Cafe Database Creation Script

-- Create the database
CREATE DATABASE IF NOT EXISTS gaming_cafe_db;
USE gaming_cafe_db;

-- Table 1: Membership (no dependencies)
CREATE TABLE Membership (
    MembershipID INT PRIMARY KEY AUTO_INCREMENT,
    MembershipType ENUM('Standard', 'Premium', 'VIP') NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE,
    Status ENUM('Active', 'Expired', 'Cancelled') DEFAULT 'Active'
);

-- Table 2: GameTitle (no dependencies)
CREATE TABLE GameTitle (
    GameID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200) NOT NULL,
    Genre VARCHAR(50),
    AgeRestriction INT DEFAULT 0,
    MaxSessionTime INT COMMENT 'in minutes',
    Platform ENUM('PC', 'Console', 'Both'),
    AvailabilityStatus ENUM('Available', 'Maintenance', 'Unavailable') DEFAULT 'Available'
);

-- Table 3: Employee (no dependencies)
CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    Role ENUM('Receptionist', 'Cashier', 'Administrator', 'AccountManager', 'GameManager') NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    ShiftStart TIME,
    ShiftEnd TIME,
    AccessLevel INT DEFAULT 1,
    PasswordHash VARCHAR(255) NOT NULL
);

-- Table 4: Promotions (no dependencies)
CREATE TABLE Promotions (
    PromoID INT PRIMARY KEY AUTO_INCREMENT,
    PromoCode VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT,
    DiscountValue DECIMAL(10,2),
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    IsActive BOOLEAN DEFAULT TRUE
);

-- Table 5: UserAccount (depends on Membership)
CREATE TABLE UserAccount (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(15),
    IsMinor BOOLEAN,
    GuardianID INT,
    MembershipID INT,
    JoinDate DATE DEFAULT (CURRENT_DATE),
    CreditBalance DECIMAL(10,2) DEFAULT 0.00,
    AccountStatus ENUM('Active', 'Suspended', 'Deleted') DEFAULT 'Active',
    PasswordHash VARCHAR(255) NOT NULL,
    FOREIGN KEY (GuardianID) REFERENCES UserAccount(UserID) ON DELETE SET NULL,
    FOREIGN KEY (MembershipID) REFERENCES Membership(MembershipID) ON DELETE SET NULL
);

-- Table 6: Station (no dependencies)
CREATE TABLE Station (
    StationID INT PRIMARY KEY AUTO_INCREMENT,
    StationType ENUM('PC', 'Console') NOT NULL,
    Location VARCHAR(100),
    Status ENUM('Available', 'Occupied', 'Maintenance') DEFAULT 'Available',
    AssignedUserID INT,
    FOREIGN KEY (AssignedUserID) REFERENCES UserAccount(UserID) ON DELETE SET NULL
);

-- Table 7: GameSession (depends on UserAccount, GameTitle, Station)
CREATE TABLE GameSession (
    SessionID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    StationID INT NOT NULL,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME,
    SessionStatus ENUM('Active', 'Paused', 'Finished', 'Cancelled') DEFAULT 'Active',
    TotalTimePlayed INT DEFAULT 0 COMMENT 'in minutes',
    FOREIGN KEY (UserID) REFERENCES UserAccount(UserID) ON DELETE CASCADE,
    FOREIGN KEY (GameID) REFERENCES GameTitle(GameID) ON DELETE CASCADE,
    FOREIGN KEY (StationID) REFERENCES Station(StationID) ON DELETE CASCADE
);

-- Table 8: Payment (depends on UserAccount, Employee, Promotions)
CREATE TABLE Payment (
    InvoiceID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    EmployeeID INT,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentDateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'Account Credit') NOT NULL,
    PromoApplied INT,
    FOREIGN KEY (UserID) REFERENCES UserAccount(UserID) ON DELETE CASCADE,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID) ON DELETE SET NULL,
    FOREIGN KEY (PromoApplied) REFERENCES Promotions(PromoID) ON DELETE SET NULL
);

-- Add indexes for better query performance
CREATE INDEX idx_user_email ON UserAccount(Email);
CREATE INDEX idx_user_status ON UserAccount(AccountStatus);
CREATE INDEX idx_session_user ON GameSession(UserID);
CREATE INDEX idx_session_status ON GameSession(SessionStatus);
CREATE INDEX idx_game_title ON GameTitle(Title);
CREATE INDEX idx_payment_user ON Payment(UserID);
CREATE INDEX idx_payment_date ON Payment(PaymentDateTime);

-- Show all tables created
SHOW TABLES;