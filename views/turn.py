"""turn view"""
from views.base import View


class TurnView(View):

    @classmethod
    def show_the_matchs(cls, matchs):
        i = 1
        for match in matchs:
            print(f"Match {i}:\n{match}")
            input("Suivant ->")
            i += 1

    @classmethod
    def end_of_the_matchs(cls):
        print(f"\n"
              f"{'-' * 30} FIN DES MATCHS {'-' * 30}")
        input("-- RENTRER LES SCORES: ----> \n"
              "")

    @classmethod
    def ask_player_score(cls, player):
        return input(f"Score de {player}: ")

