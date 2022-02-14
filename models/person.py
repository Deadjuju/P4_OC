"""Classes Person and Player"""

from tinydb import where
from typing import List

from initialisation import PLAYERS_TABLE


class Person:
    """Person"""

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 gender: str,
                 date_of_birth: str):
        """Has a first_name, a last_name, a gender and a birthday"""
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return f"👥 {self.full_name}"

    def __str__(self) -> str:
        return f"👥 {self.full_name}"

    @property
    def full_name(self) -> str:
        """Return Full Name"""
        return f"{self.first_name} {self.last_name}"


class Player(Person):
    """Class Player"""

    def __init__(self,
                 first_name,
                 last_name,
                 gender,
                 date_of_birth,
                 ranking: int = 0,
                 tournament_score: float = 0,
                 already_faced=None,
                 alphabetical=False):
        super().__init__(first_name, last_name, gender, date_of_birth)
        if already_faced is None:
            already_faced = []
        self.ranking = ranking
        self.tournament_score = tournament_score
        self.already_faced = already_faced
        self.alphabetical = alphabetical

    def __str__(self) -> str:
        return f"{super().__str__()} #{self.ranking}"

    def __repr__(self) -> str:
        return f"{super().__str__()} - #{self.ranking} - 🎂 {self.date_of_birth}"

    def __lt__(self, other):
        if self.alphabetical:
            return self.first_name < other.first_name
        return self.ranking < other.ranking

    @property
    def db_instance(self) -> dict:
        """ Return an instance of player from the database, or None

                Returns:
                    (dict): instance of player
                """
        return PLAYERS_TABLE.get((where('first_name') == self.first_name)
                                 & (where('last_name') == self.last_name))

    @classmethod
    def search_player(cls, first_name, last_name) -> List:
        """List of players with same characteristics

                Args:
                    first_name (str): first name of player
                    last_name (str): last name of player
                Returns:
                    list_players_dictionary (list): players

                """

        list_players_dictionary = PLAYERS_TABLE.search(
            (where('first_name') == first_name)
            & (where('last_name') == last_name)
        )
        return list_players_dictionary

    @classmethod
    def update_attribute(cls, new_attribute_value, attribute_name: str, player_id: int):
        """update an attribute in database

                Args:
                    new_attribute_value (): new value
                    attribute_name (str): attribut's name
                    player_id (int): id of player
                """
        player_id_list = [player_id]
        PLAYERS_TABLE.update({attribute_name: new_attribute_value},
                             doc_ids=player_id_list)

    @classmethod
    def delete_a_player(cls, player_id):
        """delete a player from database

                Args:
                    player_id (int): id of player
                """
        player_id_list = [player_id]
        PLAYERS_TABLE.remove(doc_ids=player_id_list)

    @classmethod
    def get_players_instances_list(cls, players_id_list: List[int]) -> List:
        """Generate list of Players instances

                Args:
                    players_id_list (list): list of ids players
                Returns:
                    instances_players_list (list): list of Players Instances
                """

        instances_players_list = []
        for player_id in players_id_list:
            player_dict: dict = PLAYERS_TABLE.get(doc_id=player_id)
            players_instance = Player(**player_dict)
            instances_players_list.append(players_instance)
        return instances_players_list

    def save(self) -> int:
        """ Save an instance of a player in the database

                Returns:
                    (int): id of player in database
                """
        player_table = PLAYERS_TABLE
        return player_table.insert(self.__dict__)

    def exists(self) -> bool:
        """ Return True if instance exist in database

                Returns:
                    (bool)
                """

        return bool(self.db_instance)


if __name__ == "__main__":
    player_1 = Player(first_name="Robert",
                      last_name="Garcia",
                      gender="Male",
                      date_of_birth="04/08/1991",
                      ranking=1)

    print(player_1)
    print(player_1.__repr__())
