import sys
from pathlib import Path
from typing import List

from initialisation import PLAYERS_TABLE, TOURNAMENTS_TABLE
from controllers.tournamentsmanager import TournamentController
from models.match import Match
from models.person import Player
from models.tournament import Tournament
from models.turn import Turn


class Reports:
    """Generate and export report"""
    def __init__(self, view, export: bool = False, title_report: str = "", file_name: str = ""):
        self.view = view
        self.export = export
        self.title_report = title_report
        self.file_name = file_name

    @classmethod
    def export_in_txt(cls, list_to_export: List[Player], file_name: str, title: str):
        """Export report in format txt
            Args:
                list_to_export (List[Player]): list of player instances
                file_name (str): name of the file to save
                title (str): title name in file
                """

        path_to_extract = Path(__file__).resolve().parent.parent / "reports"
        path_to_extract.mkdir(exist_ok=True)
        path = path_to_extract / file_name
        with open(path, "a", encoding='utf8') as file:
            file.write(f"{title}\n\n")
        with open(path, "a", encoding='utf8') as file:
            for element in list_to_export:
                file.write(f"•  {element}\n\n")

    def display_run(self, elements_list: List):
        """Display report and export it in format txt if wanted
            Args:
                elements_list (List): list of class (Player, Tournaments, Turns or Matchs) instances
                """
        self.view.display_report(title=self.title_report, elements_list=elements_list)
        if self.export:
            self.export_in_txt(list_to_export=elements_list,
                               file_name=self.file_name,
                               title=self.title_report)


class ReportsController:
    def __init__(self, view, player_view, tournament_view):
        self.view = view
        self.player_view = player_view
        self.tournament_view = tournament_view

    def choose_a_report(self) -> str:
        """Ask and check a report's choice
                Returns:
                    (str): Choice of report
                """
        while True:
            choice = self.view.prompt_for_report_choice()
            if choice == "1":
                return "all players"
            if choice == "2":
                return "all tournaments"
            if choice == "3":
                return "select tournament"
            if choice == "4":
                return "return"
            if choice == "off":
                return "off"
            else:
                self.view.warning("Choix non autorisé")

    def choose_ranking_or_alphabetical(self):
        """Ask and check a display mode
                Returns:
                    (str): display mode
                """

        while True:
            display_mode = self.view.prompt_for_ranking_pr_alphabetical_report()
            if display_mode == "1":
                return "ranking"
            if display_mode == "2":
                return "alphabetical"
            if display_mode == "off":
                return "off"
            else:
                self.view.warning("Choix non autorisé")

    def choose_display_option_tournament(self):
        """Ask and check a display option for a tournament
                Returns:
                    (str): display option
                """

        while True:
            display_option = self.view.prompt_for_display_option_tournament()
            if display_option == "1":
                return "ranking"
            if display_option == "2":
                return "alphabetical"
            if display_option == "3":
                return "turns"
            if display_option == "4":
                return "matchs"
            if display_option == "off":
                return "off"
            else:
                self.view.warning("Choix non autorisé")

    def generate_a_report(self):
        """execution and selection of the different choices to generate a report"""

        # display players
        report_run = True
        while report_run:
            report_choice = self.choose_a_report()

            if report_choice == "all players":
                sorted_report = self.choose_ranking_or_alphabetical()
                if sorted_report == "off":
                    sys.exit()
                # get list of Players instances
                players_dict_list = PLAYERS_TABLE.all()
                players_list = [Player(**dict) for dict in players_dict_list]

                # sort the list of Players instances
                if sorted_report == "ranking":
                    players_list.sort()
                    rapport = Reports(view=self.view,
                                      export=True,
                                      title_report="TOUS LES JOUEURS",
                                      file_name="players_ranking.txt")
                    rapport.display_run(elements_list=players_list)

                if sorted_report == "alphabetical":
                    players_list_alphabet = []
                    for player_instance in players_list:
                        player_instance.alphabetical = True
                        players_list_alphabet.append(player_instance)
                    players_list_alphabet.sort()
                    rapport = Reports(view=self.view,
                                      export=True,
                                      title_report="TOUS LES JOUEURS",
                                      file_name="players_alphabetical.txt")
                    rapport.display_run(elements_list=players_list_alphabet)

            # display tournaments
            if report_choice == "all tournaments":
                tournaments_dict_list = TOURNAMENTS_TABLE.all()
                tournaments_list = [Tournament(**dict) for dict in tournaments_dict_list]
                rapport = Reports(view=self.view,
                                  export=True,
                                  title_report="TOUS LES TOURNOIS",
                                  file_name="tournaments.txt")
                rapport.display_run(elements_list=tournaments_list)

            # rapport for a tournament
            if report_choice == "select tournament":
                self.view.information(message="---- CHARGER UN TOURNOIS ----")
                tournaments_controller = TournamentController(view=self.tournament_view,
                                                              player_view=self.player_view)
                tournaments_list = tournaments_controller.find_tournaments_list()

                if len(tournaments_list) == 1:
                    tournament_dict = tournaments_list[0]
                    tournament = Tournament(**tournament_dict)
                    self.tournament_view.show_the_tournament_found(tournament=True)
                    self.tournament_view.information(message=tournament)

                    players_id_list = tournament.players

                    players_unsorted_list = Player.get_players_instances_list(
                        players_id_list=players_id_list
                    )

                    sorted_rapport_choice = self.choose_display_option_tournament()
                    # Tournament / Player Ranking
                    if sorted_rapport_choice == "off":
                        sys.exit()
                    if sorted_rapport_choice == "ranking":
                        players_unsorted_list.sort()
                        rapport = Reports(view=self.view,
                                          export=True,
                                          title_report="LISTE DES JOUEURS:",
                                          file_name=f"{tournament.tournament_name}_ranking_players.txt")
                        rapport.display_run(elements_list=players_unsorted_list)

                    # Tournament / Player alphabetical
                    if sorted_rapport_choice == "alphabetical":
                        players_list = []
                        for player_instance in players_unsorted_list:
                            player_instance.alphabetical = True
                            players_list.append(player_instance)
                        players_list.sort()
                        rapport = Reports(view=self.view,
                                          export=True,
                                          title_report="LISTE DES JOUEURS:",
                                          file_name=f"{tournament.tournament_name}_alphabetical_players.txt")
                        rapport.display_run(elements_list=players_list)

                    # Turns & Matchs / Tournament
                    if sorted_rapport_choice == "turns" or sorted_rapport_choice == "matchs":
                        turns_id_list = tournament.turns
                        instances_turns_list = Turn.get_turns_instances_list(turns_id_list=turns_id_list)

                        # Turns
                        if sorted_rapport_choice == "turns":
                            rapport = Reports(view=self.view,
                                              export=False,
                                              title_report="LISTE DES TOURS:",
                                              file_name=f"{tournament.tournament_name}_turns.txt")
                            rapport.display_run(elements_list=instances_turns_list)

                        # Matchs
                        if sorted_rapport_choice == "matchs":
                            matchs_id_list = []
                            for turn_instance in instances_turns_list:
                                matchs_id_list += turn_instance.matchs
                            instances_matchs_list = Match.get_matchs_instances_list(matchs_id_list=matchs_id_list)
                            rapport = Reports(view=self.view,
                                              export=False,
                                              title_report="LISTE DES MATCHS:",
                                              file_name=f"{tournament.tournament_name}_matchs.txt")
                            rapport.display_run(elements_list=instances_matchs_list)

                if len(tournaments_list) == 0:
                    self.tournament_view.show_the_tournament_found(tournament=False)

            if report_choice == "return":
                report_run = False

            if report_choice == "off":
                sys.exit()


if __name__ == '__main__':
    from views.player import PlayerView
    from views.reports import ReportsView
    from views.tournament import TournamentView

    player_view = PlayerView()
    tournament_view = TournamentView()
    rapports_view = ReportsView()
    test = ReportsController(view=rapports_view, player_view=player_view, tournament_view=tournament_view)
    test.generate_a_report()
