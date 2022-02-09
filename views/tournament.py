"""Player view."""

from views.base import View


class TournamentView(View):
    """Implement the other views."""

    @classmethod
    def prompt_to_create_tournament_or_load_it(cls):
        print("Que voulez-vous faire? Tapez:")
        return input(f"|{'-' * 42}|\n"
                     "| 1  --> Pour créer un tournois -----------|\n"
                     "| 2  --> Pour charger un tournois ---------|\n"
                     "| 3  --> Pour revenir en arrière ----------|\n"
                     f"|{'-' * 42}|"
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_tournament_name(cls):
        """Prompt for a tournament name."""
        return input(f"Nom du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_tournament_place(cls):
        """Prompt for a tournament name."""
        return input(f"Lieu de déroulement du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_start_date(cls):
        """Prompt for a beginning date."""
        return input(f"Date de début du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_end_date(cls):
        """Prompt for a ending date."""
        return input(f"Date de fin du tournois: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_description(cls):
        """Prompt for Tournament description."""
        return input(f"Entrez une description du tournois: "
                     f"{View.CURSOR}")

    # @classmethod
    # def prompt_for_time_control(cls):
    #     """Prompt for Tournament time control's mode."""
    #     return input(f"|| {'_' * 50}\n"
    #                  f"|| Quel le mode de control du temps?\n"
    #                  f"|| Tapez :\n"
    #                  f"|| 1 --> Bullet\n"
    #                  f"|| 2 --> Blitz\n"
    #                  f"|| 3 --> Coup rapide\n"
    #                  f"|| {'_' * 50}"
    #                  f"{View.CURSOR}")
    #
    @classmethod
    def show_the_tournament_found(cls, tournament: bool):
        if tournament:
            print(f"|{'-' * 70}|\n"
                  f"|--> ℹ️INFORMATION ℹ️: Tournois trouvé dans la base de donnée.\n"
                  f"|{'-' * 70}|")
        else:
            print(f"|{'-' * 50}|\n"
                  "|--> ℹ️INFORMATION ℹ️: Ce tournois n'existe pas dans la base de données.\n"
                  f"|{'-' * 50}|")



