-- SJSU CMPE 138 FALL 2025 TEAM1
-- Views Creation Script

USE gaming_cafe_db;

-- View 1: Active Sessions with User and Game Info
CREATE OR REPLACE VIEW ActiveSessions AS
SELECT 
    gs.SessionID,
    u.FullName AS PlayerName,
    u.Email,
    gt.Title AS GameTitle,
    gt.Genre,
    s.StationID,
    s.StationType,
    s.Location,
    gs.StartTime,
    gs.TotalTimePlayed,
    (gt.MaxSessionTime - gs.TotalTimePlayed) AS TimeRemaining
FROM GameSession gs
JOIN UserAccount u ON gs.UserID = u.UserID
JOIN GameTitle gt ON gs.GameID = gt.GameID
JOIN Station s ON gs.StationID = s.StationID
WHERE gs.SessionStatus = 'Active';

-- View 2: User Account Summary with Membership Info
CREATE OR REPLACE VIEW UserAccountSummary AS
SELECT 
    u.UserID,
    u.FullName,
    u.Email,
    u.DateOfBirth,
    TIMESTAMPDIFF(YEAR, u.DateOfBirth, CURDATE()) AS Age,
    u.IsMinor,
    m.MembershipType,
    m.Status AS MembershipStatus,
    u.CreditBalance,
    u.AccountStatus,
    COUNT(DISTINCT gs.SessionID) AS TotalSessions
FROM UserAccount u
LEFT JOIN Membership m ON u.MembershipID = m.MembershipID
LEFT JOIN GameSession gs ON u.UserID = gs.UserID
GROUP BY u.UserID, u.FullName, u.Email, u.DateOfBirth, u.IsMinor, 
         m.MembershipType, m.Status, u.CreditBalance, u.AccountStatus;

-- View 3: Revenue Report
CREATE OR REPLACE VIEW RevenueReport AS
SELECT 
    DATE(p.PaymentDateTime) AS PaymentDate,
    COUNT(p.InvoiceID) AS TotalTransactions,
    SUM(p.Amount) AS TotalRevenue,
    AVG(p.Amount) AS AverageTransaction,
    SUM(CASE WHEN p.PromoApplied IS NOT NULL THEN 1 ELSE 0 END) AS TransactionsWithPromo
FROM Payment p
GROUP BY DATE(p.PaymentDateTime)
ORDER BY PaymentDate DESC;

-- View 4: Game Popularity
CREATE OR REPLACE VIEW GamePopularity AS
SELECT 
    gt.GameID,
    gt.Title,
    gt.Genre,
    gt.Platform,
    COUNT(gs.SessionID) AS TotalSessions,
    SUM(gs.TotalTimePlayed) AS TotalMinutesPlayed,
    AVG(gs.TotalTimePlayed) AS AvgSessionLength
FROM GameTitle gt
LEFT JOIN GameSession gs ON gt.GameID = gs.GameID
GROUP BY gt.GameID, gt.Title, gt.Genre, gt.Platform
ORDER BY TotalSessions DESC;

-- Test the views
SELECT * FROM ActiveSessions;
SELECT * FROM UserAccountSummary LIMIT 5;
SELECT * FROM RevenueReport;
SELECT * FROM GamePopularity;