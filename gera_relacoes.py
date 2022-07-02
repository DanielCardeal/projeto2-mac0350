#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from random import randint, random
from typing import Optional

NAMES_FILE = "./names.txt"


@dataclass
class Args:
    """Argumentos de linha de comando"""

    output_type: str
    num_people: int
    friendship_chance: float


@dataclass(init=False)
class Person:
    """Um indivíduo na base de dados"""

    name: str
    id: int

    def __init__(self, name: str) -> None:
        self.name = name
        self.id = randint(0, 2**20)


@dataclass
class Friendship:
    """Uma entrada na tabela de amigos amizades"""

    person_id: int
    friend_id: int
    person_name: str
    friend_name: str


def parseArgs() -> Optional[Args]:
    """Lê e interpreta os argumentos de linha de comando"""
    argv = sys.argv
    argc = len(argv)
    print(argv)
    if argc != 4:
        return
    if argv[1] != "postgres" and argv[1] != "neo4j":
        return
    output = argv[1]
    num_people = int(argv[2])
    relation_percent = float(argv[3])
    return Args(output, num_people, relation_percent)


def getPersonList(args: Args) -> list[Person]:
    """Gera e devolve uma lista de pessoas usando o arquivo de nomes"""
    people = None
    with open(NAMES_FILE, "r") as names_file:
        names = names_file.readlines()[: args.num_people]
        people = [Person(str.strip(name)) for name in names]
    return people


def createFriendships(args: Args, personList: list[Person]) -> list[Friendship]:
    """Gera uma lista de amizades a partir das pessoas na lista de pessoas"""
    friendships = []
    for i in range(len(personList)):
        person = personList[i]
        for friend in personList[i + 1 :]:
            if random() > args.friendship_chance:
                continue
            # Aleatoriza quem é amigo de quem, para permitir diversidade na db
            if random() >= 0.5:
                friendships.append(Friendship(person.id, friend.id, person.name, friend.name))
            else:
                friendships.append(Friendship(friend.id, person.id, friend.name, person.name))
    return friendships


def printInsertSQL(personList: list[Person], friendshipList: list[Friendship]) -> None:
    """Cria o SQL de insert para as pessoas e amizades"""
    # SQL para PERSON
    personString = ",\n\t".join(
        [f"({person.id:12d}, '{person.name:s}')" for person in personList]
    )
    print(f"INSERT INTO PERSON(ID, Name)\nVALUES\n\t{personString};")
    print()
    # SQL para FRIENDSHIP
    friendshipString = ",\n\t".join(
        [
            f"({friendship.person_id:12d}, {friendship.friend_id:12d})"
            for friendship in friendshipList
        ]
    )
    print(f"INSERT INTO FRIENDSHIP(PersonId, FriendId)\nVALUES\n\t{friendshipString};")


def printInsertNeo(personList: list[Person], friendshipList: list[Friendship]) -> None:
    personString = ",\n\t".join(
        [f"({person.name}:PERSON{{name:'{person.name}'}})" for person in personList]
    )
    print(f"CREATE\n\t{personString}")
    print()
    friendshipString = ",\n\t".join(
        [
            f"({friendship.person_name})-[:FRIENDSHIP]->({friendship.friend_name})"
            for friendship in friendshipList
        ]
    )
    print(f"CREATE\n\t{friendshipString}")

    


# --- Main
if __name__ == "__main__":
    args = parseArgs()
    if args is None:
        print("Argumentos inválidos!")
        exit(1)
    personList = getPersonList(args)
    friendships = createFriendships(args, personList)
    # OUTPUT
    print(f"Número de amizades geradas: {len(friendships)}", file=sys.stderr)
    if args.output_type == "postgres":
        printInsertSQL(personList, friendships)
    elif args.output_type == "neo4j":
        printInsertNeo(personList, friendships)
