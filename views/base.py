"""Base view."""


class PlayerView:
    """Implement the other views."""

    def ask_create_player_or_upload_ranking(self):
        print("Que voulez-vous faire? Tapez:")
        return input("1  --> Pour créer un joueur \n"
                     "2  --> Pour mettre à jour le classement\n"
                     "3  --> Pour revenir en arrière\n"
                     "----->  || ")

    def prompt_for_player_first_name(self):
        """Prompt for a first name."""
        return input("Prénom du joueur: ")

    def prompt_for_player_last_name(self):
        """Prompt for a last name."""
        return input("Nom de famille du joueur: ")

    def prompt_for_player_gender(self):
        """Prompt for a gender."""
        return input("Genre du joueur (Femme / Homme): ")

    def prompt_for_player_date_of_birth(self):
        """Prompt for a birthday."""
        return input("Date de naissance du joueur (Format: jj/mm/aaaa): ")

    def prompt_yes_or_no(self):
        """Prompt Yes or No"""
        return input("Y/n ")
