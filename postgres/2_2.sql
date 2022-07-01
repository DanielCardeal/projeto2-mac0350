-- "Quem tem amizade com Bob?"
SELECT amigo.ID, amigo.Name
FROM PERSON AS amigo, PERSON AS bob, FRIENDSHIP AS f
WHERE amigo.ID = f.PersonId AND bob.ID = f.FriendId AND bob.Name = 'Bob';
