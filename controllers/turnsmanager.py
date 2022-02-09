from controllers.base import Controller
from controllers.pairsgeneration import GenerationOfPairs
from models.match import Match
from models.person import Player
from models.turn import Turn


class TurnsManager(Controller):

    def __init__(self, view, tournament_name, turn_number: int, players_id_list: list):
        super().__init__(view)
        self.view = view
        self.tournament_name = tournament_name
        self.turn_number = turn_number
        self.players_id_list = players_id_list
        self.pairs_generate = GenerationOfPairs(players_id_list=players_id_list)

    def _checks_results(self, player):
        while True:
            player_score = input(f"Score de {player}: ")
            if player_score == "0":
                return 0
            if player_score == "0.5" or player_score == "0,5":
                return 0.5
            if player_score == "1":
                return 1
            else:
                self.view.warning("Ce choix n'est pas autorisé.")

    @classmethod
    def save_player_score(cls, player, player_score):
        first_name = player.split(" ")[1]
        last_name = player.split(" ")[2]
        players_list = Player.search_player(first_name=first_name,
                                            last_name=last_name)
        player = players_list[0]
        player_id = player.doc_id
        instance_player = Player(**player)
        instance_player.tournament_score += player_score
        print(instance_player.tournament_score)
        print(first_name, last_name)
        instance_player.update_attribute(
            new_attribute_value=instance_player.tournament_score,
            attribute_name="tournament_score",
            player_id=player_id
        )

    def ask_and_check_players_score(self, match):

        self.view.information(message="Rentrez\n"
                                      "0 -> pour une défaite\n"
                                      "0.5 -> pour un nul\n"
                                      "1 -> pour une victoire\n"
                                      f"----- {match} -----")
        player1_score = self._checks_results(player=match.player_1)
        self.save_player_score(player=match.player_1,
                               player_score=player1_score)

        player2_score = self._checks_results(player=match.player_2)
        self.save_player_score(player=match.player_2,
                               player_score=player2_score)

        return player1_score, player2_score

    def turns_run(self):
        pairs = self.pairs_generate.swiss_system()

        matchs_list = [
            Match(player_1=pair[0].__str__(), player_2=pair[1].__str__()) for pair in pairs
        ]

        turn = Turn(tournament_name=self.tournament_name,
                    matchs=matchs_list,
                    current_turn_number=self.turn_number)

        self.view.show_the_matchs(matchs=turn.matchs)
        while self.check_yes_or_no(
                message="Voulez-vous revoir les matchs du tournois: ",
                subject=self.tournament_name,
                commit_message=("--- Voir les Matchs ---", "")
        ):
            self.view.show_the_matchs(matchs=turn.matchs)

        self.view.end_of_the_matchs()
        # Type the matchs results
        id_matchs_list = []
        for match in matchs_list:
            match_results = self.ask_and_check_players_score(match=match)
            # change score
            match.score_player_1 = match_results[0]
            match.score_player_2 = match_results[1]
            # save match end get id
            id_match = match.save()
            id_matchs_list.append(id_match)
            print(f"ID MATCH: {id_match}")

        turn.matchs = id_matchs_list

        # print(turn.__dict__)
        # for match in turn.matchs:
        #     print(match)
        #
        return turn


if __name__ == '__main__':
    from views.turn import TurnView

    players_id_list = [1, 2, 6, 8, 3, 4, 5, 7]
    turn_in_progress = TurnsManager(view=TurnView,
                                    tournament_name="Tournois test",
                                    turn_number=1,
                                    players_id_list=players_id_list)
    turn_in_progress.turns_run()
