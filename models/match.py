"""Match"""


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
    def match_name(self):
        return [{self.player_1}, {self.score_player_1}], [{self.player_2}, {self.score_player_2}]



