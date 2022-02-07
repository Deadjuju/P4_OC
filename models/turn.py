"""Turn"""
from datetime import datetime

from initialisation import DATE_FORMAT, HOURS_FORMAT


class Turn:
    """Turn in a tournament"""

    def __init__(self, tournament_name, matchs=None, current_turn_number: int = 0):
        self.tournament_name = tournament_name
        if matchs is None:
            matchs = []
        self.matchs = matchs
        self.current_turn_number = current_turn_number
        self.tour_name = f"Round {self.current_turn_number}"
        self.start_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")
        self.end_date_and_time = None

    def __str__(self):
        return f"{self.tournament_name} - {self.current_turn_number}\n" \
               f"{self.matchs}"

    def get_end_date(self):
        self.end_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")


if __name__ == '__main__':
    turn1 = Turn(tournament_name="Test", matchs=[], current_turn_number=1)

    print(turn1.__dict__)
    turn1.get_end_date()
    print(turn1.__dict__)
