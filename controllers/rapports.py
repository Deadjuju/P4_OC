import sys
from pathlib import Path

from controllers.tournamentsmanager import TournamentController, FindTournament
from initialisation import PLAYERS_TABLE, TOURNAMENTS_TABLE, TURNS_TABLE, MATCHS_TABLE
from models.match import Match
from models.person import Player
from models.tournament import Tournament
from models.turn import Turn
from views.tournament import TournamentView


class Rapports:
    def __init__(self, export: bool = False, title_report="", doc_name=""):
        self.export = export
        self.title_report = title_report
        self.doc_name = doc_name

    @classmethod
    def export_in_txt(cls, list_to_export, doc_name, title):
        path = Path(__file__).resolve().parent.parent / doc_name
        with open(path, "a", encoding='utf8') as file:
            file.write(f"{title}\n\n")
        with open(path, "a", encoding='utf8') as file:
            for element in list_to_export:
                file.write(f"•  {element}\n\n")

    @classmethod
    def display_report(cls, title, elements_list):
        print(title)
        for element in elements_list:
            print(element)
            print("-" * 50)

    def display_run(self, elements_list):
        self.display_report(title=self.title_report, elements_list=elements_list)
        if self.export:
            self.export_in_txt(list_to_export=elements_list,
                               doc_name=self.doc_name,
                               title=self.title_report)


class RapportsController:
    def __init__(self, view, tournament_view):
        self.view = view
        self.tournament_view = tournament_view
        self.find_tournament = FindTournament(view=tournament_view)

    @classmethod
    def choose_a_rapport(cls) -> str:
        while True:
            choice = input("Choix:\n"
                           "1 - Pour afficher tous les joueurs\n"
                           "2 - Pour afficher les tournois\n"
                           "3 - Pour choisir un tournois et afficher ses détails\n"
                           "4 - Retour"
                           "--> ")
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
                print("Choix non autorisé")

    @classmethod
    def choose_ranking_or_alphabetical(cls):
        while True:
            choice = input("Choix:\n"
                           "1 - Pour afficher les joueurs par ordre de classement \n"
                           "2 - Pour afficher les joueurs par ordre alphabétique\n"
                           "--> ")
            if choice == "1":
                return "ranking"
            if choice == "2":
                return "alphabetical"
            else:
                print("Choix non autorisé")

    @classmethod
    def choose_display_option_tournament(cls):
        while True:
            choice = input("Choix:\n"
                           "1 - Pour afficher les joueurs par ordre de classement \n"
                           "2 - Pour afficher les joueurs par ordre alphabétique\n"
                           "3 - Pour afficher tous les tours du tournois\n"
                           "4 - Pour afficher tous les matchs du tournois\n"
                           "--> ")
            if choice == "1":
                return "ranking"
            if choice == "2":
                return "alphabetical"
            if choice == "3":
                return "turns"
            if choice == "4":
                return "matchs"
            else:
                print("Choix non autorisé")

    def generate_a_rapport(self):

        # display players
        rapport_run = True
        while rapport_run:
            rapport_choice = self.choose_a_rapport()

            if rapport_choice == "all players":
                sorted_rapport = self.choose_ranking_or_alphabetical()
                players_dict_list = PLAYERS_TABLE.all()
                players_list = [Player(**dict) for dict in players_dict_list]
                if sorted_rapport == "ranking":
                    players_list.sort()
                    rapport = Rapports(export=True,
                                       title_report="TOUS LES JOUEURS",
                                       doc_name="players_ranking.txt")
                    rapport.display_run(elements_list=players_list)

                if sorted_rapport == "alphabetical":
                    players_list_alphabet = []
                    for player_instance in players_list:
                        player_instance.alphabetical = True
                        players_list_alphabet.append(player_instance)

                    players_list_alphabet.sort()
                    rapport = Rapports(export=True,
                                       title_report="TOUS LES JOUEURS",
                                       doc_name="players_alphabetical.txt")
                    rapport.display_run(elements_list=players_list_alphabet)

            # display tournaments
            if rapport_choice == "all tournaments":
                tournaments_dict_list = TOURNAMENTS_TABLE.all()
                tournaments_list = [Tournament(**dict) for dict in tournaments_dict_list]
                rapport = Rapports(export=True,
                                   title_report="TOUS LES TOURNOIS",
                                   doc_name="tournaments.txt")
                rapport.display_run(elements_list=tournaments_list)

            # rapport for a tournament
            if rapport_choice == "select tournament":
                self.tournament_view.information(message="---- CHARGER UN TOURNOIS ----")
                tournaments_list = self.find_tournament.find_tournaments_list()

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
                    if sorted_rapport_choice == "ranking":
                        players_unsorted_list.sort()
                        rapport = Rapports(export=True,
                                           title_report="LISTE DES JOUEURS:",
                                           doc_name=f"{tournament.tournament_name}_ranking_players.txt")
                        rapport.display_run(elements_list=players_unsorted_list)

                    # Tournament / Player alphabetical
                    if sorted_rapport_choice == "alphabetical":
                        players_list = []
                        for player_instance in players_unsorted_list:
                            player_instance.alphabetical = True
                            players_list.append(player_instance)
                        players_list.sort()
                        rapport = Rapports(export=True,
                                           title_report="LISTE DES JOUEURS:",
                                           doc_name=f"{tournament.tournament_name}_alphabetical_players.txt")
                        rapport.display_run(elements_list=players_list)

                    # Turns & Matchs / Tournament
                    if sorted_rapport_choice == "turns" or sorted_rapport_choice == "matchs":
                        turns_id_list = tournament.turns
                        instances_turns_list = Turn.get_turns_instances_list(turns_id_list=turns_id_list)

                        # Turns
                        if sorted_rapport_choice == "turns":
                            rapport = Rapports(export=False,
                                               title_report="LISTE DES TOURS:",
                                               doc_name=f"{tournament.tournament_name}_turns.txt")
                            rapport.display_run(elements_list=instances_turns_list)

                        # Matchs
                        if sorted_rapport_choice == "matchs":
                            matchs_id_list = []
                            for turn_instance in instances_turns_list:
                                matchs_id_list += turn_instance.matchs
                            instances_matchs_list = Match.get_matchs_instances_list(matchs_id_list=matchs_id_list)
                            rapport = Rapports(export=False,
                                               title_report="LISTE DES MATCHS:",
                                               doc_name=f"{tournament.tournament_name}_matchs.txt")
                            rapport.display_run(elements_list=instances_matchs_list)

                if len(tournaments_list) == 0:
                    self.tournament_view.show_the_tournament_found(tournament=False)

            if rapport_choice == "return":
                rapport_run = False

            if rapport_choice == "off":
                sys.exit()


if __name__ == '__main__':
    tournament_manager = TournamentView()
    test = RapportsController(view="", tournament_view=tournament_manager)
    test.generate_a_rapport()

    # rapport = Rapports(table=PLAYERS_TABLE)
    # print(rapport.get_table)
