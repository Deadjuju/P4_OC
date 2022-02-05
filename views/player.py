"""Player view."""

from views.base import View


class PlayerView(View):
    """Implement the other views."""

    @classmethod
    def prompt_to_create_player_or_upload_ranking(cls):
        print("Que voulez-vous faire? Tapez:")
        return input(f"|{'-' * 70}|\n"
                     "| 1  -->  Pour créer un joueur   --------------------------------------|\n"
                     "| 2  -->  Pour mettre à jour le classement / supprimer un joueur   ----|\n"
                     "| 3  -->  Pour revenir en arrière   -----------------------------------|\n"
                     f"|{'-' * 70}|"
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_player_first_name(cls):
        """Prompt for a first name."""
        return input(f"Prénom du joueur: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_player_last_name(cls):
        """Prompt for a last name."""
        return input("Nom de famille du joueur: "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_player_gender(cls):
        """Prompt for a gender."""
        return input("Genre du joueur (Femme / Homme): "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_for_player_date_of_birth(cls):
        """Prompt for a birthday."""
        return input("Date de naissance du joueur (Format: jj/mm/aaaa): "
                     f"{View.CURSOR}")

    @classmethod
    def prompt_to_edit_or_delete_player(cls):
        """Ask Edit a Player or delete a Player"""
        print("Voulez-vous:\n"
              "--> 1 pour changer le classement d'un joueur\n"
              "--> 2 pour supprimer un joueur")
        return input(f"1/2 {View.CURSOR}")

    @classmethod
    def prompt_to_change_score(cls):
        """Ask for a new rating"""
        while True:
            new_score_str = input("Quel est le nouveau classement de ce joueur?"
                                  f"\n{View.CURSOR}")
            if new_score_str.isnumeric():
                return int(new_score_str)
            print()
            print("Merci de rentrer un nombre.")

    @classmethod
    def show_the_player_found(cls, player: bool):
        if player:
            print(f"|{'-' * 70}|\n"
                  f"|--> ℹ️INFORMATION ℹ️: Joueur trouvé dans la base de donnée.\n"
                  f"|{'-' * 70}|")
        else:
            print(f"|{'-' * 50}|\n"
                  "|--> ℹ️INFORMATION ℹ️: Ce joueur n'existe pas.\n"
                  f"|{'-' * 50}|")

    @classmethod
    def print_the_edit_delete_choice(cls, choice):
        if choice == "edit":
            print("Classement du joueur correctement mis à jour")
        if choice == "delete":
            print("Joueur correctement supprimé")

