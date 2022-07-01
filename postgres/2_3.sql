-- "Quem são os amigo(a)s dos amigo(a)s de Alice"
-- ============ Variáveis =============
-- * alice    => Alice
-- * f_al     => Amizades de alice
-- * f_am     => Amizades do amigo de alice
-- * amigo_am => Amigo do amigo
select amigo_am.ID, amigo_am.Name
from PERSON as alice
join FRIENDSHIP as f_al on f_al.PersonId = alice.ID
join FRIENDSHIP as f_am on f_am.PersonId = f_al.FriendId
join PERSON as amigo_am on amigo_am.ID = f_am.FriendId
where alice.Name = 'Alice';
