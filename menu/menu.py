import sys

from controllers.playersmanager import PlayerController
from controllers.reports import ReportsController
from controllers.tournamentsmanager import TournamentController
from views.base import View


class MenuView(View):

    @classmethod
    def prompt_for_menu_choice(cls):
        print("__________________________________________________\n"
              "__________________________________________________\n"
              "*********         MENU PRINCIPAL         *********\n"
              "__________________________________________________\n"
              "__________________________________________________\n")
        choice = input("****    Pour gérer les joueurs, tapez '1'\n"
                       "****    Pour gérer les tournois, tapez '2'\n"
                       "****    Pour générer des rapports, tappez '3'\n"
                       "****    Pour quitter, tappez 'off'"
                       f"{View.CURSOR}  ")
        return choice


class MainMenu:

    def __init__(self, view, player_view, tournament_view, reports_view):
        self.view = view
        self.player_view = player_view
        self.tournament_view = tournament_view
        self.reports_view = reports_view

    def _ask_and_check_menu_choice(self) -> str:
        """ask to user to make a choice and control it

                Returns:
                    (str): user choice
                """

        while True:
            choice = self.view.prompt_for_menu_choice()
            if choice == "1":
                return "1"
            if choice == "2":
                return "2"
            if choice == "3":
                return "3"
            if choice == "off":
                return "off"
            else:
                self.view.warning(message="Cette réponse n'est pas autorisé")

    def menu_run(self):

        choice = self._ask_and_check_menu_choice()

        if choice == "1":
            player_control = PlayerController(view=self.player_view)
            player_control.players_manager()

        if choice == "2":
            tournament_control = TournamentController(view=self.tournament_view,
                                                      player_view=self.player_view)
            tournament_control.tournaments_manager()

        if choice == "3":
            report_control = ReportsController(view=self.reports_view,
                                               player_view=self.player_view,
                                               tournament_view=self.tournament_view)
            report_control.generate_a_report()

        if choice == "off":
            sys.exit()


if __name__ == '__main__':
    from views.player import PlayerView
    from views.tournament import TournamentView
    from views.reports import ReportsView

    menu_view = MenuView
    player_view = PlayerView()
    tournament_view = TournamentView()
    reports_view = ReportsView()

    main_menu = MainMenu(view=menu_view,
                         player_view=player_view,
                         tournament_view=tournament_view,
                         reports_view=reports_view)
    main_menu.menu_run()
