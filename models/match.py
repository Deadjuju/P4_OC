"""Model Match"""

from typing import Tuple, List

from initialisation import MATCHS_TABLE
from models.person import Player

Player_PlayerScore = List[str]


class Match:
    """Match class: Two players with their score """

    def __init__(self,
                 player_1: Player,
                 player_2: Player,
                 score_player_1: float = 0,
                 score_player_2: float = 0):
        self.player_1 = player_1
        self.player_2 = player_2

        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    def __str__(self):
        return f"([{self.player_1}, {self.score_player_1}], [{self.player_2}, {self.score_player_2}])"

    def __repr__(self):
        return f"([{self.player_1}, {self.score_player_1}], [{self.player_2}, {self.score_player_2}])"

    @property
    def match_name(self) -> Tuple[Player_PlayerScore, Player_PlayerScore]:
        """Returns the name of a match in the format ([player1, score1], [player2, score2])
            Returns:
                (tuple): name of the match
                """

        return [f"{self.player_1}, {self.score_player_1}"], [f"{self.player_2}, {self.score_player_2}"]

    @classmethod
    def get_matchs_instances_list(cls, matchs_id_list: List[int]) -> List:
        """Generate list of Match instances

                Args:
                    matchs_id_list (list): list of ids matchs
                Returns:
                    instances_matchs_list (list): list of Matchs Instances
                """

        instances_matchs_list = []
        # get all turn's instance
        for match_id in matchs_id_list:
            match_dict: dict = MATCHS_TABLE.get(doc_id=match_id)
            matchs_instance = Match(**match_dict)
            instances_matchs_list.append(matchs_instance)
        return instances_matchs_list

    def save(self) -> int:
        """ Save an instance of a match in the database

                Returns:
                    (int): id of match in database
                """
        matchs_table = MATCHS_TABLE
        return matchs_table.insert(self.__dict__)


