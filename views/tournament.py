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


