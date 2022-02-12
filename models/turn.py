"""Turn"""
from datetime import datetime

from initialisation import DATE_FORMAT, HOURS_FORMAT, TURNS_TABLE


class Turn:
    """Turn in a tournament"""

    def __init__(self, tournament_name: str,
                 matchs=None,
                 current_turn_number: int = 0,
                 start_date_and_time: str = "",
                 end_date_and_time: str = ""):
        self.tournament_name = tournament_name
        if matchs is None:
            matchs = []
        self.matchs = matchs
        self.current_turn_number = current_turn_number
        self.start_date_and_time = start_date_and_time
        if start_date_and_time == "":
            self.get_start_date()
        self.end_date_and_time = end_date_and_time

    @property
    def tour_name(self):
        return f"Round {self.current_turn_number}"

    @property
    def dates(self):
        return f"{self.start_date_and_time} | {self.end_date_and_time}"

    def __str__(self):
        return f"{self.tournament_name} - {self.tour_name}\n" \
               f"{self.dates}\n"

    def __repr__(self):
        return f"{self.tournament_name} - {self.tour_name}\n" \
               f"{self.dates}\n"

    @classmethod
    def get_turns_instances_list(cls, turns_id_list) -> list:
        instances_turns_list = []
        # get all turn's instance
        for turn_id in turns_id_list:
            turn_dict: dict = TURNS_TABLE.get(doc_id=turn_id)
            turns_instance = Turn(**turn_dict)
            instances_turns_list.append(turns_instance)
        return instances_turns_list

    def get_start_date(self):
        """Get the date when the round starts """
        self.start_date_and_time = datetime.now().strftime(f"{DATE_FORMAT[0]} {HOURS_FORMAT}")

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
