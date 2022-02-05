"""Tournament"""

from models.person import Player
from models.timecontrol import TimeControl
from models.turn import Turn


DEFAULT_NUMBER_OF_TURNS = 4


class Tournament:
    """Has a Name, a Place, a Date (Start + End) and a description"""

    def __init__(self,
                 name: str,
                 place: str,
                 start_date,
                 end_date,
                 description: str,
                 time_control,
                 is_finish: bool = False):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_turns = DEFAULT_NUMBER_OF_TURNS
        self.turns: list[Turn] = []
        self.players: list[int] = []
        self.competing_players: list[int] = []
        self.time_control = time_control
        self.is_finish = is_finish

    def __str__(self) -> str:
        return f"{self.name} - {self.place}\nDate: {self.date}\n{self.description}"

    def __repr__(self) -> str:
        return f"{self.name} - {self.place}\nDate: {self.date}\n{self.description}"

    @property
    def date(self) -> tuple:
        return self.start_date, self.end_date


if __name__ == "__main__":
    tournament_1 = Tournament(name="FlammekuEchec",
                              place="Strasbourg",
                              start_date="30/01/2022",
                              end_date="31/01/2022",
                              description="1er tournoi d'échec du fameux AlsaChess Tour.",
                              time_control="Bullet")
    print(tournament_1.date)
    print(tournament_1.__str__())
    print(tournament_1.__dict__)

