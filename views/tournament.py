"""Tournament view."""

from views.base import View


class TournamentView(View):
    """Tournament views."""

    @classmethod
    def prompt_to_create_tournament_or_load_it(cls) -> str:
        """
        :return: user choice
        """

        print("Que voulez-vous faire? Tapez:")
        return input(f""
                     f"\n"
                     f"|{'-' * 76}|\n"
                     "|______________________||   > GESTION DE TOURNOIS    ||______________________|\n"
                     "|   1    ---> Pour créer un tournois    -------------------------------------|\n"
                     "|   2    --->  Pour charger un tournois et l'exécuter    --------------------|\n"
                     "|   off  --->  Pour quitter le programme    ---------------------------------|\n"
                     f"|{'-' * 76}|"
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_tournament_name(cls) -> str:
        """Prompt for a tournament name."""
        return input(f"Nom du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_tournament_place(cls) -> str:
        """Prompt for a tournament name."""
        return input(f"Lieu de déroulement du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_start_date(cls) -> str:
        """Prompt for a beginning date."""
        return input(f"Date de début du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_end_date(cls) -> str:
        """Prompt for a ending date."""
        return input(f"Date de fin du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_description(cls) -> str:
        """Prompt for Tournament description."""
        return input(f"Entrez une description du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def show_the_tournament_found(cls, tournament: bool):
        """
        display tournament
        :param tournament: tournament to display
        """
        if tournament:
            print(f"|{'-' * 70}|\n"
                  f"|--> ℹ️INFORMATION ℹ️: Tournois trouvé dans la base de donnée.\n"
                  f"|{'-' * 70}|")
        else:
            print(f"|{'-' * 50}|\n"
                  "|--> ℹ️INFORMATION ℹ️: Ce tournois n'existe pas dans la base de données.\n"
                  f"|{'-' * 50}|")
