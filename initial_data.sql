-- Insert users into auth_user
INSERT INTO auth_user (id, username, password, email, first_name, last_name, is_staff, is_active, is_superuser, date_joined)
VALUES
    (1, 'user1', '12345', 'user1@example.com', 'Emre', 'Ulusan', TRUE, TRUE, FALSE, NOW()),
    (2, 'user2', '12345', 'user2@example.com', 'Yunus', 'Ulusan', TRUE, TRUE, FALSE, NOW()),
    (3, 'user3', '12345', 'user3@example.com', 'Mehmet', 'Delice', TRUE, TRUE, FALSE, NOW()),
    (4, 'user4', '12345', 'user4@example.com', 'Burak', 'Kutlu', TRUE, TRUE, FALSE, NOW()),
    (5, 'user5', '12345', 'user5@example.com', 'Ahmet', 'Kayra', TRUE, TRUE, FALSE, NOW());

-- Insert teams into parts_team
INSERT INTO parts_team (id, name, description)
VALUES
    (1, 'wing', 'Wing Team'),
    (2, 'fuselage', 'Fuselage Team'),
    (3, 'tail', 'Tail Team'),
    (4, 'avionics', 'Avionics Team'),
    (5, 'assembly', 'Assembly Team');

-- Insert parts into parts_part
INSERT INTO parts_part (id, name, quantity, team_id, aircraft, is_used)
VALUES
    (5, 'wing', 5, 1, 'tb2', FALSE),
    (6, 'fuselage', 3, 2, 'tb3', FALSE),
    (7, 'tail', 4, 3, 'akinci', FALSE),
    (8, 'avionics', 6, 4, 'kizilelma', FALSE);

-- Insert aircraft into parts_aircraft
INSERT INTO parts_aircraft (id, name, produced_date)
VALUES
    (1, 'tb2', NOW()),
    (2, 'tb3', NOW()),
    (3, 'akinci', NOW()),
    (4, 'kizilelma', NOW());


INSERT INTO parts_team_users (team_id, user_id)
VALUES
    (1, 1), 
    (2, 2), 
    (3, 3), 
    (4, 4), 
    (5, 5),
    (3, 1),
    (2, 3);


INSERT INTO parts_aircraft_parts (aircraft_id, part_id)
VALUES
    (1, 5), -- 'wing' part for 'tb2'
    (2, 6), -- 'fuselage' part for 'tb3'
    (3, 7), -- 'tail' part for 'akinci'
    (4, 8); -- 'avionics' part for 'kizilelma'
