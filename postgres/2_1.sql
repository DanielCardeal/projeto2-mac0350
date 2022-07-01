-- "Quem são os amigos de Bob?"
SELECT amigo.ID, amigo.Name
FROM PERSON bob
JOIN FRIENDSHIP as f on f.PersonId = bob.ID
JOIN PERSON as amigo on amigo.ID = f.FriendId
WHERE bob.Name = 'Bob';
