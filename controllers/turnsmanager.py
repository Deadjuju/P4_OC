from controllers.base import Controller
from controllers.pairsgeneration import GenerationOfPairs
from models.match import Match
from models.person import Player
from models.turn import Turn


class TurnsManager(Controller):
    """ TurnsManager Controller"""

    def __init__(self,
                 view,
                 tournament_name,
                 turn_number: int,
                 players_id_list: list):
        super().__init__(view)
        self.tournament_name = tournament_name
        self.turn_number = turn_number
        self.players_id_list = players_id_list
        self.pairs_generate = GenerationOfPairs(players_id_list=players_id_list)

    def display_matchs(self, turn: Turn):
        """Display each match: pairs of players

                Args:
                    turn (Turn): actual turn
                """

        self.view.show_the_matchs(matchs=turn.matchs)
        while self.check_yes_or_no(
                message="Voulez-vous revoir les matchs du tournois: ",
                subject=self.tournament_name,
                commit_message=("--- Voir les Matchs ---", "")
        ):
            self.view.show_the_matchs(matchs=turn.matchs)

    def _ask_and_checks_results(self, player) -> float:
        """ask to type a result from a player and check it

                Args:
                    player (): name of the player
                Returns:
                    (float): player score
                """

        while True:
            player_score = self.view.ask_question(question=f"Score de {player}: ")
            if player_score == "0":
                return 0
            if player_score == "0.5" or player_score == "0,5":
                return 0.5
            if player_score == "1":
                return 1
            else:
                self.view.warning("Ce choix n'est pas autorisé.")

    @classmethod
    def _save_player_score(cls, player: str, player_score: float):
        """upload the player score in database (Player)

                Args:
                    player (str): name of the player (unformatted name)
                    player_score (float): player score
                """

        first_name = player.split(" ")[1]
        last_name = player.split(" ")[2]
        players_list = Player.search_player(first_name=first_name,
                                            last_name=last_name)
        player = players_list[0]
        player_id = player.doc_id
        instance_player = Player(**player)
        instance_player.tournament_score += player_score
        instance_player.update_attribute(
            new_attribute_value=instance_player.tournament_score,
            attribute_name="tournament_score",
            player_id=player_id
        )

    def get_players_score(self, match: Match) -> tuple:
        """Get score for each players from a match

                Args:
                    match (Match): Match's instance
                Return:
                    (tuple): (player1_score, player2_score)
                """

        self.view.information(message="Rentrez\n"
                                      "0 -> pour une défaite\n"
                                      "0.5 -> pour un nul\n"
                                      "1 -> pour une victoire\n"
                                      f"----- {match} -----")
        player1_score = self._ask_and_checks_results(player=match.player_1)
        self._save_player_score(player=str(match.player_1),
                                player_score=player1_score)

        player2_score = self._ask_and_checks_results(player=match.player_2)
        self._save_player_score(player=str(match.player_2),
                                player_score=player2_score)

        return player1_score, player2_score

    def turns_run(self) -> Turn:
        """creation of a turn and course of it """
        pairs = self.pairs_generate.swiss_system()

        matchs_list = [
            Match(player_1=pair[0].__str__(), player_2=pair[1].__str__()) for pair in pairs
        ]

        turn = Turn(tournament_name=self.tournament_name,
                    matchs=matchs_list,
                    current_turn_number=self.turn_number)

        self.display_matchs(turn=turn)

        self.view.end_of_the_matchs()

        # Type the matchs results
        id_matchs_list = []
        for match in matchs_list:
            match_results = self.get_players_score(match=match)
            # change score
            match.score_player_1 = match_results[0]
            match.score_player_2 = match_results[1]
            # save match end get id
            id_match = match.save()
            id_matchs_list.append(id_match)

        turn.matchs = id_matchs_list

        return turn


if __name__ == '__main__':
    from views.turn import TurnView

    players_id_list_for_test = [1, 2, 6, 8, 3, 4, 5, 7]
    turn_in_progress = TurnsManager(view=TurnView,
                                    tournament_name="Tournois test",
                                    turn_number=1,
                                    players_id_list=players_id_list_for_test)
    turn_in_progress.turns_run()
