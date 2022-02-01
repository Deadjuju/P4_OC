"""Person and Player"""

import datetime
from pathlib import Path
from tinydb import TinyDB, where


class Person:
    """Person"""

    def __init__(self, first_name: str, last_name: str, gender, date_of_birth):
        """Has a first_name, a last_name, a gender and a birthday"""
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return f"{self.full_name}"

    def __str__(self) -> str:
        return f"{self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")


class Player(Person):
    """Class Player"""

    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

    def __init__(self, first_name, last_name, gender, date_of_birth, ranking: int):
        """Has a first_name, a last_name, a gender and a birthday
        Has a ranking"""
        super().__init__(first_name, last_name, gender, date_of_birth)
        self.ranking = ranking
        self.score: float = 0

    def __str__(self) -> str:
        return f"{super().__str__()} #{self.ranking}"

    def save(self) -> int:
        player_table = Player.DB.table("Players")
        return player_table.insert(self.__dict__)


if __name__ == "__main__":
    player_1 = Player(first_name="Julien",
                      last_name="Garcia",
                      gender="male",
                      date_of_birth="04/08/1991",
                      ranking=1)

    print(player_1)
