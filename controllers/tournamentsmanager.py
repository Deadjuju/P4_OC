import sys

from controllers.base import Controller
from models.person import Player
from models.tournament import Tournament
from views.player import PlayerView


class TournamentController(Controller):

    def __init__(self, view, player_view):
        super().__init__(view)
        self.player_view = player_view

    def _check_ask_create_tournament_or_load_tournament(self):
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

    def ask_and_check_time_control_field(self):
        while True:
            time_control_choice = self.view.prompt_for_time_control()
            if time_control_choice == "1":
                return "Bullet"
            elif time_control_choice == "2":
                return "Blitz"
            elif time_control_choice == "3":
                return "Coup rapide"
            else:
                self.view.warning(message="Merci de renseigner 1, 2 ou 3.")

    def _create_tournament(self) -> Tournament:
        tournament_name = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_name,
            message="Le champ - Place - ne peut pas être vide."
        ).title()
        tournament_place = self._ask_and_check_field(
            field=self.view.prompt_for_tournament_place,
            message="Le champ - Place - ne peut pas être vide."
        ).title()
        start_date = self._ask_and_check_field_date(field=self.view.prompt_for_start_date)
        end_date = self._ask_and_check_field_date(field=self.view.prompt_for_end_date)
        description = self.view.prompt_for_description()
        time_control = self.ask_and_check_time_control_field()
        tournament = Tournament(tournament_name=tournament_name,
                                place=tournament_place,
                                start_date=start_date,
                                end_date=end_date,
                                description=description,
                                time_control=time_control)
        return tournament

    def get_players(self):
        participants = []
        for i in range(8):
            inscription = True
            while inscription:
                print(f"Joueur {i + 1}")
                player_first_name = self._ask_and_check_field(
                    field=self.player_view.prompt_for_player_first_name,
                    message="Le champ - prénom - ne peut pas être vide."
                ).title()
                player_last_name = self._ask_and_check_field(
                    field=self.player_view.prompt_for_player_last_name,
                    message="Le champ - nom - ne peut pas être vide."
                ).title()
                player = Player.search_player(first_name=player_first_name,
                                              last_name=player_last_name)

                try:
                    player_id = player[0].doc_id
                except IndexError:
                    print("Ce joueur n'est pas enregistré.")
                else:
                    if player_id not in participants:
                        participants.append(player_id)
                        print(player)
                        i += 1
                        inscription = False
                    else:
                        print("Ce joueur est déjà inscrit au tournois.")
        print(participants)
        return participants

    def tournaments_manager(self):
        """execution and selection of the different choices"""
        tournaments_manager_run = True
        while tournaments_manager_run:
            choice = self._check_ask_create_tournament_or_load_tournament()
            if choice == "off":
                self.view.information(message="A BIENTOT!!!")
                sys.exit()
            if choice == "1":
                tournament = self._create_tournament()
                participants = self.get_players()
                tournament.players = participants
                tournament.competing_players = participants
                print(tournament.__dict__)
                if not tournament.exists():
                    if self.check_yes_or_no(message="Voulez-vous sauvegarder le tournois: ",
                                            subject=tournament.__dict__):
                        tournament.save()
                else:
                    self.view.warning(message="Ce tournois existe déjà.")


if __name__ == '__main__':
    from views.tournament import TournamentView

    tournament_manager = TournamentView()
    player_view = PlayerView()
    tournament_control = TournamentController(view=tournament_manager, player_view=player_view)
    tournament_control.tournaments_manager()
    # tournament = tournament_control._create_tournament()
    # print(tournament.__dict__)
