from pathlib import Path

from initialisation import PLAYERS_TABLE, TOURNAMENTS_TABLE
from models.person import Player
from models.tournament import Tournament


class Rapports:
    def __init__(self, table):
        self.table = table

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


class PlayersRapports(Rapports):
    def __init__(self, table, alphabetical: bool = False, export: bool = False):
        super().__init__(table)
        self.alphabetical = alphabetical
        self.export = export

        self.title_report = "LISTE DES JOUEURS PAR ORDRE DE CLASSEMENT:"
        self.doc_name = "players_ranking.txt"
        if self.alphabetical:
            self.title_report = "LISTE DES JOUEURS PAR ORDRE ALPHABETIQUE:"
            self.doc_name = "players_alphabetical.txt"

    def generate_sorted_players(self):
        players_list = []
        for player_dict in self.get_table:
            player_instance = Player(**player_dict)
            if self.alphabetical:
                player_instance.alphabetical = True
            players_list.append(player_instance)
        players_list.sort()
        return players_list

    def sort_players_and_display(self):
        sorted_players = self.generate_sorted_players()
        self.display_report(title=self.title_report, elements_list=sorted_players)
        if self.export:
            self.export_in_txt(list_to_export=sorted_players,
                               doc_name=self.doc_name,
                               title=self.title_report)


class RapportsController:
    def __init__(self, view):
        self.view = view

    @classmethod
    def choose_a_rapport(cls):
        while True:
            choice = input("Choix:\n"
                           "1 - Pour afficher tous les joueurs\n"
                           "2 - Pour afficher les tournois\n"
                           "4 - Pour choisir in tournois et afficher ses détails\n"
                           "--> ")
            if choice == "1":
                return "all players"
            if choice == "2":
                return "all tournaments"
            else:
                print("Choix non autorisé")

    def ranking_or_alphabetical(self):
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

    def generate_a_rapport(self):
        rapport_choice = self.choose_a_rapport()

        if rapport_choice == "all players":
            sorted_rapport = self.ranking_or_alphabetical()
            if sorted_rapport == "ranking":
                rapport = PlayersRapports(table=PLAYERS_TABLE)
                rapport.sort_players_and_display()
            if sorted_rapport == "alphabetical":
                rapport = PlayersRapports(table=PLAYERS_TABLE, alphabetical=True)
                rapport.sort_players_and_display()


        #     self.player_sorted_ranking()
        # if rapport_choice == "all alphabetical players":
        #     self.player_sorted_alphabetical()
        # if rapport_choice == "all tournaments":
        #     self.player_sorted_alphabetical()


if __name__ == '__main__':

    test = RapportsController(view="")
    test.generate_a_rapport()

    # rapport_tournaments = Rapports(table=TOURNAMENTS_TABLE)
    # tournaments_list = rapport_tournaments.generate_tournaments_list()
    # rapport_tournaments.export_in_txt(list_to_export=tournaments_list,
    #                                   doc_name="tournaments.txt",
    #                                   title="LISTE DES TOURNOIS")


