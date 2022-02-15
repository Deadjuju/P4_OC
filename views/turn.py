"""turn view"""

from views.base import View


class TurnView(View):
    """ Turns View """

    @classmethod
    def show_the_matchs(cls, matchs):
        """
        dipslay matchs
        :param matchs: match to display
        """
        i = 1
        for match in matchs:
            print(f"Match {i}:\n{match}")
            input("Suivant ->")
            i += 1

    @classmethod
    def end_of_the_matchs(cls):
        """ Indicates the end of the generations of the pairs """
        print(f"\n"
              f"{'-' * 30} FIN DES MATCHS {'-' * 30}")
        print("-- RENTRER LES SCORES: ----> \n"
              "")

    @classmethod
    def ask_player_score(cls, player) -> str:
        """
        :param player: concerned player
        :return: Player Score
        """
        return input(f"Score de {player}: ")
