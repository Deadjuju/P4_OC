from time import sleep
import sys
from typing import List

from controllers.base import Controller
from controllers.turnsmanager import TurnsManager
from models.person import Player
from models.tournament import Tournament
from models.turn import Turn
from views.turn import TurnView
from initialisation import DEFAULT_NUMBER_OF_TURNS, NUMBERS_OF_PLAYERS


class TournamentController(Controller):
    """ Tournament Controller """

    def __init__(self, view, player_view):
        super().__init__(view)
        self.player_view = player_view

    def _check_ask_create_tournament_or_load_tournament(self) -> str:
        """ask to user to make a choice about tournaments

                Returns:
                    (str): user choice
                """

        while True:
            choice = self.view.prompt_to_create_tournament_or_load_it()
            if choice == "1":
                return "1"
            elif choice == "2":
                return "2"
            elif choice.lower() == "return" or choice.lower() == "retour" or choice == "3":
                return "return"
            elif choice == "off":
                return "off"
            else:
                self.view.warning(message="Merci de renseigner 1, 2 ou 3.")

    def ask_and_check_time_control_field(self) -> str:
        """Prompt to choose a time control mode

                Returns:
                    (str): time control mode
                """

        question = f"|| {'_' * 50}\n" \
                   f"|| Quel le mode de control du temps?\n" \
                   f"|| Tapez :\n" \
                   f"|| 1 --> Bullet\n" \
                   f"|| 2 --> Blitz\n" \
                   f"|| 3 --> Coup rapide\n" \
                   f"|| {'_' * 50}" \
                   f"{self.view.CURSOR}"
        message = "Merci de renseigner 1, 2 ou 3."
        responses = {"1": "Bullet",
                     "Bullet": "Bullet",
                     "bullet": "Bullet",
                     "2": "Blitz",
                     "Blitz": "Blitz",
                     "blitz": "Blitz",
                     "3": "Coup rapide",
                     "Rapide": "Coup rapide",
                     "rapide": "rapide"}
        return self.control_list_of_user_choices(responses_list=responses,
                                                 question=question,
                                                 message=message)

    def _create_tournament(self) -> Tournament:
        """
                Returns:
                    tournament (Tournament): instance of a tournament
                """

        tournament_name = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_name,
            message="Le champ - Place - ne peut pas être vide."
        ).title()
        tournament_place = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_place,
            message="Le champ - Place - ne peut pas être vide."
        ).title()
        start_date = self._ask_and_check_field_date(
            field=self.view.prompt_for_start_date
        )
        end_date = self._ask_and_check_field_date(
            field=self.view.prompt_for_end_date
        )
        description = self.view.prompt_for_description()
        time_control = self.ask_and_check_time_control_field()

        tournament = Tournament(tournament_name=tournament_name,
                                tournament_place=tournament_place,
                                start_date=start_date,
                                end_date=end_date,
                                description=description,
                                number_of_turns=DEFAULT_NUMBER_OF_TURNS,
                                time_control=time_control)
        return tournament

    def _save_tournament(self, tournament: Tournament) -> bool:
        """Check if the tournament does not exist and save it
            Args:
                tournament (Tournament): tournament's instance
            Return:
                (bool)
                """

        if not tournament.exists():
            if self.check_yes_or_no(
                    message="Voulez-vous sauvegarder le tournois: ",
                    subject=tournament.__dict__,
                    commit_message=("--- SAUVEGARDE ---", "--- ABANDONS ---")
            ):
                tournament.save()
                return True
        else:
            self.view.warning(message="Ce tournois existe déjà.")
            return False

    def _get_players(self) -> List[int]:
        """Generates list of players

                Returns:
                    participants (list): list of participants
                """

        participants = []
        for i in range(NUMBERS_OF_PLAYERS):
            inscription = True
            while inscription:
                # Check if the player is in the database
                self.view.information(message=f"Joueur {i + 1}")
                player_first_name = self._ask_and_check_field(
                    field=self.player_view.prompt_for_player_first_name,
                    message="Le champ - prénom - ne peut pas être vide."
                ).title()
                player_last_name = self._ask_and_check_field(
                    field=self.player_view.prompt_for_player_last_name,
                    message="Le champ - nom - ne peut pas être vide."
                ).title()
                players_list = Player.search_player(first_name=player_first_name,
                                                    last_name=player_last_name)

                try:
                    player = players_list[0]
                except IndexError:
                    self.view.warning(message="Ce joueur n'est pas enregistré.")
                else:
                    player_id = player.doc_id
                    if player_id not in participants:

                        # initialisation: tournament_score=0 & already_faced=[]
                        player_instance = Player(**player)
                        if not player_instance.already_in_tournament:

                            participants.append(player_id)
                            print(players_list)
                            i += 1
                            inscription = False
                        else:
                            self.view.warning(message="Ce joueur participe déjà à un tournois")
                    else:
                        self.view.warning(message="Ce joueur est déjà inscrit au tournois.")
        self.view.information(message=participants)
        return participants

    @classmethod
    def _initialise_attributes(cls,
                               id_participants_lists: List[int],
                               is_in_tournament: bool):
        """Update each players in database before begining first turn"""

        for id_participant in id_participants_lists:
            Player.update_attribute(
                new_attribute_value=0,
                attribute_name="tournament_score",
                player_id=id_participant
            )
            Player.update_attribute(
                new_attribute_value=[],
                attribute_name="already_faced",
                player_id=id_participant
            )
            Player.update_attribute(
                new_attribute_value=is_in_tournament,
                attribute_name="already_in_tournament",
                player_id=id_participant
            )

    def find_tournaments_list(self) -> List:
        """Find in database the list of tournaments who have the same characteristics

                Returns:
                    (list): list of tournaments
                """

        tournament_name = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_name,
            message="Le champ - Nom - ne peut pas être vide."
        ).title()
        tournament_place = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_place,
            message="Le champ - Lieu - ne peut pas être vide."
        ).title()

        # list of players who have the same characteristics
        tournaments_table_list = Tournament.search_tournament(tournament_name=tournament_name,
                                                              tournament_place=tournament_place)
        return tournaments_table_list

    @classmethod
    def _creating_and_running_the_turn(cls, tournament) -> Turn:
        """Creation and course of a turn
            Args:
                tournament (Tournament): tournament's instance
            Returns:
                (Turn): current turn's instance
                """

        actual_turn = tournament.actual_turn
        tournament_name = tournament.tournament_name
        players_id_list = tournament.players
        turn_creating = TurnsManager(
            view=TurnView,
            tournament_name=tournament_name,
            turn_number=actual_turn,
            players_id_list=players_id_list
        )

        turn = turn_creating.turns_run()
        return turn

    @classmethod
    def update_tournament(cls, tournament, tournament_id):
        """Save news values attributes for a tournament
            Args:
                tournament (Tournament): tournament's instance
                tournament_id (int): id of tournament to update
                """

        new_actual_turn = tournament.actual_turn
        new_turns = tournament.turns
        new_is_finish = tournament.is_finish
        tournament.update_tournament_attribute(new_attribute_value=new_actual_turn,
                                               attribute_name="actual_turn",
                                               tournament_id=tournament_id)
        tournament.update_tournament_attribute(new_attribute_value=new_turns,
                                               attribute_name="turns",
                                               tournament_id=tournament_id)
        tournament.update_tournament_attribute(new_attribute_value=new_is_finish,
                                               attribute_name="is_finish",
                                               tournament_id=tournament_id)

    def tournaments_manager(self):
        """execution and selection of the different choices"""
        tournaments_manager_run = True
        while tournaments_manager_run:
            choice = self._check_ask_create_tournament_or_load_tournament()
            if choice == "off":
                # quit programme
                self.view.information(message="A BIENTOT!!!")
                sys.exit()
            if choice == "1":
                # create a tournament
                tournament = self._create_tournament()
                participants = self._get_players()
                tournament.players = participants

                if self._save_tournament(tournament=tournament):
                    self._initialise_attributes(id_participants_lists=participants,
                                                is_in_tournament=True)

            if choice == "2":
                # Load a tournament
                self.view.information(message="---- CHARGER UN TOURNOIS ----")
                sleep(0.5)
                tournaments_list = self.find_tournaments_list()
                sleep(0.5)

                if len(tournaments_list) == 1:
                    tournament_dict = tournaments_list[0]
                    tournament_id = tournament_dict.doc_id
                    tournament = Tournament(**tournament_dict)
                    self.view.show_the_tournament_found(tournament=True)
                    self.view.information(message=tournament)

                    if not tournament.is_finish:
                        sleep(1)

                        # collects the turn and stock it in the tournament
                        turn = self._creating_and_running_the_turn(tournament=tournament)

                        # save the turn in db
                        # and stock his ID in the list tournament.turns
                        turn.get_end_date()
                        id_turn = turn.save()
                        tournament.turns.append(id_turn)

                        tournament.actual_turn += 1

                        if tournament.actual_turn == DEFAULT_NUMBER_OF_TURNS + 1:
                            tournament.is_finish = True
                            participants = tournament.players
                            self._initialise_attributes(id_participants_lists=participants,
                                                        is_in_tournament=False)

                        self.view.information(message="TOURNAMENT")
                        self.view.information(message=tournament.__dict__)

                        self.update_tournament(tournament, tournament_id=tournament_id)

                    else:
                        self.view.warning(message="Ce tournoi est terminé et ne peut pas être chargé.")

                if len(tournaments_list) == 0:
                    self.view.show_the_tournament_found(tournament=False)

            if choice == "return":
                tournaments_manager_run = False


if __name__ == '__main__':
    from views.player import PlayerView
    from views.tournament import TournamentView

    tournament_manager = TournamentView()
    player_view_for_test = PlayerView()
    tournament_control = TournamentController(view=tournament_manager,
                                              player_view=player_view_for_test)
    tournament_control.tournaments_manager()
