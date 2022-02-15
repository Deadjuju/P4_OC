"""Reports view."""

from time import sleep

from views.base import View


class ReportsView(View):
    """ Reports View """

    @classmethod
    def display_report(cls, title, elements_list):
        """
        Displays each element
        :param title: reports title
        :param elements_list: element to display
        """
        print(title)
        for element in elements_list:
            print(element)
            print("-" * 50)
            sleep(0.05)
        input("Valider: ")

    def prompt_for_report_choice(self) -> str:
        """
        :return: user choice
        """
        choice = input("Tapper:\n"
                       "1 - Pour afficher tous les joueurs\n"
                       "2 - Pour afficher les tournois\n"
                       "3 - Pour choisir un tournois et afficher ses détails\n"
                       "4 - Retour"
                       f"{self.CURSOR} ")
        return choice

    def prompt_for_ranking_pr_alphabetical_report(self) -> str:
        """
        :return: user choice
        """

        choice = input("Tapper:\n"
                       "1 - Pour afficher les joueurs par ordre de classement \n"
                       "2 - Pour afficher les joueurs par ordre alphabétique\n"
                       f"{self.CURSOR} ")
        return choice

    def prompt_for_display_option_tournament(self) -> str:
        """
        :return: user choice
        """

        choice = input("Choix:\n"
                       "1 - Pour afficher les joueurs par ordre de classement \n"
                       "2 - Pour afficher les joueurs par ordre alphabétique\n"
                       "3 - Pour afficher tous les tours du tournois\n"
                       "4 - Pour afficher tous les matchs du tournois\n"
                       f"{self.CURSOR} ")
        return choice
