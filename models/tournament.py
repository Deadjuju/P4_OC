"""Tournament"""

from tinydb import where

from initialisation import DEFAULT_NUMBER_OF_TURNS, TOURNAMENTS_TABLE


class Tournament:
    """Class Tournament"""

    def __init__(self,
                 tournament_name: str,
                 tournament_place: str,
                 start_date: str,
                 end_date: str,
                 description: str,
                 number_of_turns: int = DEFAULT_NUMBER_OF_TURNS,
                 turns=None,
                 actual_turn: int = 1,
                 time_control: str = "",
                 players=None,
                 competing_players=None,
                 is_finish: bool = False):
        """Has a Name, a Place, a Date (Start + End), a description and a time control"""

        if competing_players is None:
            competing_players = []
        if players is None:
            players = []
        if turns is None:
            turns = []
        self.tournament_name = tournament_name
        self.tournament_place = tournament_place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_turns = number_of_turns
        self.actual_turn = actual_turn
        self.turns = turns
        self.players = players
        self.competing_players = competing_players
        self.time_control = time_control
        self.is_finish = is_finish

    def __str__(self) -> str:
        return f"🏆 {self.tournament_name} - {self.tournament_place}\nDate: {self.date}\n{self.description}"

    def __repr__(self) -> str:
        return str(self.__str__())

    @property
    def db_instance(self):
        """ Return an instance of tournament from the database, or None

                Returns:
                    (dict): instance of tournament
                """
        return TOURNAMENTS_TABLE.get((where('tournament_name') == self.tournament_name)
                                     & (where('place') == self.tournament_place))

    @property
    def date(self) -> tuple:
        return self.start_date, self.end_date

    def save(self) -> int:
        """ Save an instance of a tournament in the database

                Returns:
                    (int): id of tournament in database
                """
        tournament_table = TOURNAMENTS_TABLE
        return tournament_table.insert(self.__dict__)

    @classmethod
    def search_tournament(cls, tournament_name, tournament_place) -> list:
        """List of tournaments with same characteristics

                Args:
                    tournament_name (str): name of tournament
                    tournament_place (str): place where the tournament takes place
                Returns:
                    list_tournaments_dictionary (list): tournaments

                """
        print(f"Path: {TOURNAMENTS_TABLE}")
        list_tournaments_dictionary = TOURNAMENTS_TABLE.search(
            (where('tournament_name') == tournament_name)
            & (where('tournament_place') == tournament_place)
        )
        return list_tournaments_dictionary

    @classmethod
    def update_in_db(cls, new_actual_turn: int, new_turns: list, new_is_finish: bool, player_id: int):
        """update a tournament instance in database

                Args:
                    new_actual_turn (int): new ranking
                    new_turns (list): id of player
                    new_is_finish (bool): new ranking
                    player_id (int): id of player
                """
        player_id_list = [player_id]
        TOURNAMENTS_TABLE.update({'actual_turn': new_actual_turn}, doc_ids=player_id_list)
        TOURNAMENTS_TABLE.update({'turns': new_turns}, doc_ids=player_id_list)
        TOURNAMENTS_TABLE.update({'is_finish': new_is_finish}, doc_ids=player_id_list)

    def exists(self) -> bool:
        """ Return True if instance exist in database

                Returns:
                    (bool)
                """

        return bool(self.db_instance)


if __name__ == "__main__":
    tournament_1 = Tournament(tournament_name="FlammekuEchec",
                              tournament_place="Strasbourg",
                              start_date="30/01/2022",
                              end_date="31/01/2022",
                              description="1er tournoi d'échec du fameux AlsaChess Tour.",
                              time_control="Bullet")
    print(tournament_1.date)
    print(tournament_1.__str__())
    print(tournament_1.__dict__)
