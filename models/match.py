"""Match"""
from initialisation import MATCHS_TABLE


class Match:

    def __init__(self,
                 player_1,
                 player_2,
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
    def match_name(self) -> tuple:
        """Returns the name of a match in the format ([player1, score1], [player2, score2])
            Returns:
                (tuple): id of turn in database
                """

        return [{self.player_1}, {self.score_player_1}], [{self.player_2}, {self.score_player_2}]

    @classmethod
    def get_matchs_instances_list(cls, matchs_id_list) -> list:
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


