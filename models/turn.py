"""Turn"""
from datetime import datetime

from initialisation import DATE_FORMAT, HOURS_FORMAT


class Turn:
    """Turn in a tournament"""

    def __init__(self, matchs=None, number_of_turn: int = 0):
        if matchs is None:
            matchs = []
        self.matchs = matchs
        self.number_of_turn = number_of_turn
        self.tour_name = f"Round {self.number_of_turn}"
        self.start_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")
        self.end_date_and_time = None

    def get_end_date(self):
        self.end_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")


if __name__ == '__main__':
    turn1 = Turn(matchs=[], number_of_turn=1)

    print(turn1.__dict__)
    turn1.get_end_date()
    print(turn1.__dict__)
