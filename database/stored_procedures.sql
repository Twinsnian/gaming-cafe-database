-- SJSU CMPE 138 FALL 2025 TEAM1
-- Stored Procedures

USE gaming_cafe_db;

DELIMITER //

-- Procedure 1: Start a Game Session with Age Verification
CREATE PROCEDURE StartGameSession(
    IN p_UserID INT,
    IN p_GameID INT,
    IN p_StationID INT
)
BEGIN
    DECLARE user_age INT;
    DECLARE game_restriction INT;
    DECLARE user_is_minor BOOLEAN;
    
    -- Get user age and minor status
    SELECT 
        TIMESTAMPDIFF(YEAR, DateOfBirth, CURDATE()),
        IsMinor
    INTO user_age, user_is_minor
    FROM UserAccount 
    WHERE UserID = p_UserID;
    
    -- Get game age restriction
    SELECT AgeRestriction 
    INTO game_restriction 
    FROM GameTitle 
    WHERE GameID = p_GameID;
    
    -- Check age restriction
    IF user_age >= game_restriction THEN
        -- Update station status
        UPDATE Station 
        SET Status = 'Occupied', AssignedUserID = p_UserID 
        WHERE StationID = p_StationID;
        
        -- Create session
        INSERT INTO GameSession (UserID, GameID, StationID, StartTime, SessionStatus, TotalTimePlayed)
        VALUES (p_UserID, p_GameID, p_StationID, NOW(), 'Active', 0);
        
        SELECT 'Session started successfully' AS Message, LAST_INSERT_ID() AS SessionID;
    ELSE
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'User does not meet age requirement for this game';
    END IF;
END //

-- Procedure 2: End Game Session and Calculate Payment
CREATE PROCEDURE EndGameSession(
    IN p_SessionID INT,
    OUT p_AmountDue DECIMAL(10,2)
)
BEGIN
    DECLARE v_StartTime DATETIME;
    DECLARE v_TotalMinutes INT;
    DECLARE v_StationID INT;
    
    -- Get session details
    SELECT StartTime, StationID
    INTO v_StartTime, v_StationID
    FROM GameSession
    WHERE SessionID = p_SessionID;
    
    -- Calculate total time
    SET v_TotalMinutes = TIMESTAMPDIFF(MINUTE, v_StartTime, NOW());
    
    -- Update session
    UPDATE GameSession
    SET EndTime = NOW(),
        SessionStatus = 'Finished',
        TotalTimePlayed = v_TotalMinutes
    WHERE SessionID = p_SessionID;
    
    -- Free up the station
    UPDATE Station
    SET Status = 'Available',
        AssignedUserID = NULL
    WHERE StationID = v_StationID;
    
    -- Calculate payment (example: $0.50 per minute)
    SET p_AmountDue = v_TotalMinutes * 0.50;
    
    SELECT p_AmountDue AS AmountDue, v_TotalMinutes AS TotalMinutesPlayed;
END //

-- Procedure 3: Add Credit to User Account
CREATE PROCEDURE AddUserCredit(
    IN p_UserID INT,
    IN p_Amount DECIMAL(10,2),
    IN p_EmployeeID INT
)
BEGIN
    -- Add credit to user account
    UPDATE UserAccount
    SET CreditBalance = CreditBalance + p_Amount
    WHERE UserID = p_UserID;
    
    -- Record the payment
    INSERT INTO Payment (UserID, EmployeeID, Amount, PaymentMethod)
    VALUES (p_UserID, p_EmployeeID, p_Amount, 'Account Credit');
    
    SELECT 'Credit added successfully' AS Message, 
           (SELECT CreditBalance FROM UserAccount WHERE UserID = p_UserID) AS NewBalance;
END //

DELIMITER ;

-- Test the stored procedures
CALL StartGameSession(1, 1, 1);
-- CALL EndGameSession(1, @amount);
-- SELECT @amount AS 'Amount Due';