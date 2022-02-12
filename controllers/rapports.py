from pathlib import Path

from controllers.tournamentsmanager import TournamentController, FindTournament
from initialisation import PLAYERS_TABLE, TOURNAMENTS_TABLE, TURNS_TABLE
from models.person import Player
from models.tournament import Tournament
from models.turn import Turn
from views.tournament import TournamentView


class Rapports:
    def __init__(self, table, export: bool = False):
        self.table = table
        self.export = export

    @property
    def get_table(self):
        return self.table.all()

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


class PlayersRapports(Rapports):
    def __init__(self, table, alphabetical: bool = False):
        super().__init__(table)
        self.alphabetical = alphabetical

        self.title_report = "LISTE DES JOUEURS PAR ORDRE DE CLASSEMENT:"
        self.doc_name = "players_ranking.txt"
        if self.alphabetical:
            self.title_report = "LISTE DES JOUEURS PAR ORDRE ALPHABETIQUE:"
            self.doc_name = "players_alphabetical.txt"

    def generate_sorted_players(self, list_to_sort):
        players_list = []
        for player_instance in list_to_sort:
            if self.alphabetical:
                player_instance.alphabetical = True
            players_list.append(player_instance)
        players_list.sort()
        return players_list

    def sort_players_and_display(self, list_to_sort=None):
        if list_to_sort is None:
            list_to_sort = Player.make_instances_list(dict_list=self.get_table)
        sorted_players = self.generate_sorted_players(list_to_sort=list_to_sort)
        self.display_report(title=self.title_report, elements_list=sorted_players)
        if self.export:
            self.export_in_txt(list_to_export=sorted_players,
                               doc_name=self.doc_name,
                               title=self.title_report)


class TurnsRapports(Rapports):
    def __init__(self, table):
        super().__init__(table)
        self.title_report = "LISTE DES TOURS:"
        self.doc_name = "turns.txt"

    @classmethod
    def generate_turns_list(cls, turns_id_list):
        return [
            Tournament(**tournament_dict) for tournament_dict in turns_id_list
        ]

    def turns_display(self, turns_id_list):
        turns_list = self.generate_turns_list(turns_id_list=turns_id_list)
        self.display_report(title=self.title_report, elements_list=turns_list)
        if self.export:
            self.export_in_txt(list_to_export=turns_list,
                               doc_name=self.doc_name,
                               title=self.title_report)


class TournamentsRapports(Rapports):
    def __init__(self, table):
        super().__init__(table)
        self.title_report = "LISTE DES TOURNOIS:"
        self.doc_name = "tournaments.txt"

    def generate_tournaments_list(self):
        return [
            Tournament(**tournament_dict) for tournament_dict in self.get_table
        ]

    def tournaments_display(self):
        tournaments_list = self.generate_tournaments_list()
        self.display_report(title=self.title_report, elements_list=tournaments_list)
        if self.export:
            self.export_in_txt(list_to_export=tournaments_list,
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
                           "--> ")
            if choice == "1":
                return "all players"
            if choice == "2":
                return "all tournaments"
            if choice == "3":
                return "select tournament"
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
        rapport_choice = self.choose_a_rapport()

        # display players
        if rapport_choice == "all players":
            sorted_rapport = self.choose_ranking_or_alphabetical()
            if sorted_rapport == "ranking":
                rapport = PlayersRapports(table=PLAYERS_TABLE)
                rapport.sort_players_and_display()
            if sorted_rapport == "alphabetical":
                rapport = PlayersRapports(table=PLAYERS_TABLE, alphabetical=True)
                rapport.sort_players_and_display()

        # display tournaments
        if rapport_choice == "all tournaments":
            rapport = TournamentsRapports(table=TOURNAMENTS_TABLE)
            rapport.tournaments_display()

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
                    rapport = PlayersRapports(table=PLAYERS_TABLE)
                    rapport.sort_players_and_display(list_to_sort=players_unsorted_list)

                # Tournament / Player alphanbetical
                if sorted_rapport_choice == "alphabetical":
                    rapport = PlayersRapports(table=PLAYERS_TABLE, alphabetical=True)
                    rapport.sort_players_and_display(list_to_sort=players_unsorted_list)

                # Tournament / Player Ranking
                if sorted_rapport_choice == "turns":
                    print(tournament)
                    turns_id_list = tournament.turns
                    print(turns_id_list)
                    # rapport = TurnsRapports(table=TURNS_TABLE)
                    instances_turns_list = Turn.get_turns_instances_list(turns_id_list=turns_id_list)
                    print(instances_turns_list)

                # Tournament / Player Ranking
                if sorted_rapport_choice == "matchs":
                    pass

            if len(tournaments_list) == 0:
                self.tournament_view.show_the_tournament_found(tournament=False)


if __name__ == '__main__':
    tournament_manager = TournamentView()
    test = RapportsController(view="", tournament_view=tournament_manager)
    test.generate_a_rapport()

    # rapport = Rapports(table=PLAYERS_TABLE)
    # print(rapport.get_table)
