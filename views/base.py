"""Base view."""

CURSOR = "\n----->  || "


class PlayerView:
    """Implement the other views."""

    def prompt_to_create_player_or_upload_ranking(self):
        print("Que voulez-vous faire? Tapez:")
        return input("1  --> Pour créer un joueur \n"
                     "2  --> Pour mettre à jour le classement\n"
                     "3  --> Pour revenir en arrière"
                     f"{CURSOR}")

    def prompt_for_player_first_name(self):
        """Prompt for a first name."""
        return input(f"Prénom du joueur: "
                     f"{CURSOR}")

    def prompt_for_player_last_name(self):
        """Prompt for a last name."""
        return input("Nom de famille du joueur: "
                     f"{CURSOR}")

    def prompt_for_player_gender(self):
        """Prompt for a gender."""
        return input("Genre du joueur (Femme / Homme): "
                     f"{CURSOR}")

    def prompt_for_player_date_of_birth(self):
        """Prompt for a birthday."""
        return input("Date de naissance du joueur (Format: jj/mm/aaaa): "
                     f"{CURSOR}")

    def prompt_yes_or_no(self):
        """Prompt Yes or No"""
        return input(f"Y/n{CURSOR}")

    def prompt_save_or_abort(self, message, subject):
        print(message)
        print(subject)
        response = self.prompt_yes_or_no().lower()
        if response == "y" or response == "yes" or response == "oui" or response == "o":
            print("--- SAUVEGARDE ---")
            return True
        else:
            print("--- ABANDONS ---")
            return False

    def prompt_to_edit_or_delete_player(self):
        """Ask Edit a Player or delete a Player"""
        print("Voulez-vous:\n-"
              "> 1 pour changer le score d'un joueur\n"
              "-> 2 pour supprimer un joueur")
        return input(f"1/2 {CURSOR}")

