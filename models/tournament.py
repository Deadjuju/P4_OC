"""Tournament"""
from pathlib import Path
from tinydb import TinyDB, where

from models.person import Player
from models.timecontrol import TimeControl
from models.turn import Turn

TOURNAMENTS_DATABASE_NAME = "Tournaments"
DEFAULT_NUMBER_OF_TURNS = 4


class Tournament:
    """Class Tournament"""

    # Save in DataBase at Roots
    DB = TinyDB(Path(__file__).resolve().parent.parent / 'db.json', indent=4)
    TOURNAMENTS_TABLE = DB.table(TOURNAMENTS_DATABASE_NAME)

    def __init__(self,
                 tournament_name: str,
                 place: str,
                 start_date,
                 end_date,
                 description: str,
                 time_control,
                 is_finish: bool = False):
        """Has a Name, a Place, a Date (Start + End), a description and a time control"""

        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_turns = DEFAULT_NUMBER_OF_TURNS
        self.actual_turn: int = 0
        self.turns: list[Turn] = []
        self.players: list[int] = []
        self.competing_players: list[int] = []
        self.time_control = time_control
        self.is_finish = is_finish

    def __str__(self) -> str:
        return f"{self.tournament_name} - {self.place}\nDate: {self.date}\n{self.description}"

    def __repr__(self) -> str:
        return f"{self.tournament_name} - {self.place}\nDate: {self.date}\n{self.description}"

    @property
    def db_instance(self):
        """ Return an instance of tournament from the database, or None

                Returns:
                    (dict): instance of tournament
                """
        return Tournament.TOURNAMENTS_TABLE.get((where('tournament_name') == self.tournament_name)
                                                & (where('place') == self.place))

    @property
    def date(self) -> tuple:
        return self.start_date, self.end_date

    def save(self) -> int:
        """ Save an instance of a tournament in the database

                Returns:
                    (int): id of tournament in database
                """
        tournament_table = Tournament.DB.table(TOURNAMENTS_DATABASE_NAME)
        return tournament_table.insert(self.__dict__)

    def exists(self) -> bool:
        """ Return True if instance exist in database

                Returns:
                    (bool)
                """

        return bool(self.db_instance)


if __name__ == "__main__":
    tournament_1 = Tournament(tournament_name="FlammekuEchec",
                              place="Strasbourg",
                              start_date="30/01/2022",
                              end_date="31/01/2022",
                              description="1er tournoi d'échec du fameux AlsaChess Tour.",
                              time_control="Bullet")
    print(tournament_1.date)
    print(tournament_1.__str__())
    print(tournament_1.__dict__)
