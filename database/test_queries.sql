-- SJSU CMPE 138 FALL 2025 TEAM1
-- Test Queries for Various Operations

USE gaming_cafe_db;

-- ==========================================
-- ADMINISTRATIVE QUERIES
-- ==========================================

-- Query 1: Find all active members and their spending
SELECT 
    u.UserID,
    u.FullName,
    u.Email,
    m.MembershipType,
    u.CreditBalance,
    SUM(p.Amount) AS TotalSpent,
    COUNT(DISTINCT gs.SessionID) AS TotalSessions
FROM UserAccount u
JOIN Membership m ON u.MembershipID = m.MembershipID
LEFT JOIN Payment p ON u.UserID = p.UserID
LEFT JOIN GameSession gs ON u.UserID = gs.UserID
WHERE u.AccountStatus = 'Active' AND m.Status = 'Active'
GROUP BY u.UserID, u.FullName, u.Email, m.MembershipType, u.CreditBalance
ORDER BY TotalSpent DESC;

-- Query 2: Find minors and their guardians
SELECT 
    minor.UserID AS MinorID,
    minor.FullName AS MinorName,
    minor.Email AS MinorEmail,
    TIMESTAMPDIFF(YEAR, minor.DateOfBirth, CURDATE()) AS MinorAge,
    guardian.UserID AS GuardianID,
    guardian.FullName AS GuardianName,
    guardian.Email AS GuardianEmail
FROM UserAccount minor
JOIN UserAccount guardian ON minor.GuardianID = guardian.UserID
WHERE minor.IsMinor = TRUE;

-- Query 3: Games that are currently being played
SELECT 
    gt.Title AS GameTitle,
    COUNT(gs.SessionID) AS ActivePlayers,
    GROUP_CONCAT(u.FullName SEPARATOR ', ') AS Players
FROM GameSession gs
JOIN GameTitle gt ON gs.GameID = gt.GameID
JOIN UserAccount u ON gs.UserID = u.UserID
WHERE gs.SessionStatus = 'Active'
GROUP BY gt.Title;

-- Query 4: Station utilization report
SELECT 
    s.StationID,
    s.StationType,
    s.Location,
    s.Status,
    COUNT(gs.SessionID) AS TotalSessionsHosted,
    SUM(gs.TotalTimePlayed) AS TotalMinutesUsed
FROM Station s
LEFT JOIN GameSession gs ON s.StationID = gs.StationID
GROUP BY s.StationID, s.StationType, s.Location, s.Status
ORDER BY TotalSessionsHosted DESC;

-- Query 5: Revenue by payment method
SELECT 
    PaymentMethod,
    COUNT(*) AS TransactionCount,
    SUM(Amount) AS TotalRevenue,
    AVG(Amount) AS AverageTransaction
FROM Payment
GROUP BY PaymentMethod
ORDER BY TotalRevenue DESC;

-- ==========================================
-- CUSTOMER/END-USER QUERIES
-- ==========================================

-- Query 6: User's gaming history
SELECT 
    gs.SessionID,
    gt.Title AS GamePlayed,
    s.Location AS StationLocation,
    gs.StartTime,
    gs.EndTime,
    gs.TotalTimePlayed AS MinutesPlayed,
    gs.SessionStatus
FROM GameSession gs
JOIN GameTitle gt ON gs.GameID = gt.GameID
JOIN Station s ON gs.StationID = s.StationID
WHERE gs.UserID = 1  -- Replace with specific user
ORDER BY gs.StartTime DESC;

-- Query 7: Available games for a specific user (age appropriate)
SELECT 
    gt.GameID,
    gt.Title,
    gt.Genre,
    gt.Platform,
    gt.AgeRestriction,
    gt.MaxSessionTime,
    gt.AvailabilityStatus
FROM GameTitle gt
WHERE gt.AvailabilityStatus = 'Available'
  AND gt.AgeRestriction <= (
      SELECT TIMESTAMPDIFF(YEAR, DateOfBirth, CURDATE())
      FROM UserAccount
      WHERE UserID = 1  -- Replace with specific user
  )
ORDER BY gt.Title;

-- Query 8: User's payment history with promotions
SELECT 
    p.InvoiceID,
    p.Amount,
    p.PaymentDateTime,
    p.PaymentMethod,
    pr.PromoCode,
    pr.Description AS PromoDescription,
    pr.DiscountValue
FROM Payment p
LEFT JOIN Promotions pr ON p.PromoApplied = pr.PromoID
WHERE p.UserID = 1  -- Replace with specific user
ORDER BY p.PaymentDateTime DESC;

-- Query 9: Check available stations by type
SELECT 
    StationID,
    StationType,
    Location,
    Status
FROM Station
WHERE Status = 'Available'
ORDER BY StationType, StationID;

-- Query 10: Active promotions
SELECT 
    PromoID,
    PromoCode,
    Description,
    DiscountValue,
    StartDate,
    EndDate
FROM Promotions
WHERE IsActive = TRUE 
  AND CURDATE() BETWEEN StartDate AND EndDate
ORDER BY DiscountValue DESC;

-- ==========================================
-- ANALYTICS QUERIES
-- ==========================================

-- Query 11: Most popular games by total playtime
SELECT 
    gt.Title,
    gt.Genre,
    COUNT(gs.SessionID) AS TotalSessions,
    SUM(gs.TotalTimePlayed) AS TotalMinutes,
    ROUND(AVG(gs.TotalTimePlayed), 2) AS AvgSessionLength
FROM GameTitle gt
LEFT JOIN GameSession gs ON gt.GameID = gs.GameID
GROUP BY gt.Title, gt.Genre
ORDER BY TotalMinutes DESC
LIMIT 10;

-- Query 12: Peak usage times
SELECT 
    HOUR(StartTime) AS HourOfDay,
    COUNT(*) AS SessionCount,
    ROUND(AVG(TotalTimePlayed), 2) AS AvgSessionLength
FROM GameSession
WHERE SessionStatus IN ('Active', 'Finished')
GROUP BY HOUR(StartTime)
ORDER BY SessionCount DESC;

-- Query 13: Members vs Non-members spending comparison
SELECT 
    CASE 
        WHEN u.MembershipID IS NOT NULL THEN 'Member'
        ELSE 'Non-Member'
    END AS UserType,
    COUNT(DISTINCT u.UserID) AS UserCount,
    COUNT(p.InvoiceID) AS TotalTransactions,
    SUM(p.Amount) AS TotalRevenue,
    ROUND(AVG(p.Amount), 2) AS AvgTransaction
FROM UserAccount u
LEFT JOIN Payment p ON u.UserID = p.UserID
GROUP BY UserType;

-- Query 14: Employees by role and their transaction count
SELECT 
    e.EmployeeID,
    e.FullName,
    e.Role,
    COUNT(p.InvoiceID) AS TransactionsProcessed,
    SUM(p.Amount) AS TotalAmountProcessed
FROM Employee e
LEFT JOIN Payment p ON e.EmployeeID = p.EmployeeID
GROUP BY e.EmployeeID, e.FullName, e.Role
ORDER BY TransactionsProcessed DESC;

-- Query 15: Users who exceeded max session time
SELECT 
    u.FullName,
    gt.Title AS GameTitle,
    gt.MaxSessionTime AS MaxAllowed,
    gs.TotalTimePlayed AS ActualTime,
    (gs.TotalTimePlayed - gt.MaxSessionTime) AS Overtime
FROM GameSession gs
JOIN UserAccount u ON gs.UserID = u.UserID
JOIN GameTitle gt ON gs.GameID = gt.GameID
WHERE gs.TotalTimePlayed > gt.MaxSessionTime
  AND gt.MaxSessionTime IS NOT NULL
ORDER BY Overtime DESC;