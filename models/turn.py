"""Turn"""
from datetime import datetime

from initialisation import DATE_FORMAT, HOURS_FORMAT, TURNS_TABLE


class Turn:
    """Turn in a tournament"""

    def __init__(self, tournament_name: str, matchs=None, current_turn_number: int = 0):
        self.tournament_name = tournament_name
        if matchs is None:
            matchs = []
        self.matchs = matchs
        self.current_turn_number = current_turn_number
        self.tour_name = f"Round {self.current_turn_number}"
        self.start_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")
        self.end_date_and_time = None

    def __str__(self):
        return f"{self.tournament_name} - {self.tour_name}\n" \
               f"{self.matchs}"

    def __repr__(self):
        return f"{self.tournament_name} - {self.tour_name}\n" \
               f"{self.matchs}"

    def get_end_date(self):
        """Get the date when the round ends """
        self.end_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")

    def save(self) -> int:
        """ Save an instance of a turn in the database

                Returns:
                    (int): id of turn in database
                """
        turns_table = TURNS_TABLE
        return turns_table.insert(self.__dict__)


if __name__ == '__main__':
    turn1 = Turn(tournament_name="Test", matchs=[], current_turn_number=1)

    print(turn1.__dict__)
    turn1.get_end_date()
    print(turn1.__dict__)
