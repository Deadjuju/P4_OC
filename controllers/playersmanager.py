import datetime
import sys

from models.person import Player


class Controller:

    def __init__(self, view):
        self.view = view

    def _check_ask_create_player_or_upload_score(self):
        while True:
            choice = self.view.prompt_to_create_player_or_upload_ranking()
            if choice == "1":
                return "1"
            elif choice == "2":
                return "2"
            elif choice.lower() == "return" or choice.lower() == "retour" or choice == "3":
                return "return"
            elif choice == "off":
                return "off"
            else:
                print()
                print("Merci de renseigner 1, 2 ou 3.")

    def _ask_first_name(self):
        while True:
            first_name = self.view.prompt_for_player_first_name().title()
            if first_name != "":
                return first_name
            else:
                print()
                print("Le champ - prénom - ne peut pas être vide.")

    def _ask_last_name(self):
        while True:
            last_name = self.view.prompt_for_player_last_name().title()
            if last_name != "":
                return last_name
            else:
                print()
                print("Le champ - nom de famille - ne peut pas être vide.")

    def _ask_gender(self):
        while True:
            gender = self.view.prompt_for_player_gender().lower()
            if gender == "femme" or gender == "female":
                return "Female"
            elif gender == "homme" or gender == "male":
                return "Male"
            else:
                print()
                print("Merci de renseigner un genre valide.")

    def _ask_birthday(self):
        while True:
            date_of_birth = self.view.prompt_for_player_date_of_birth()
            try:
                datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
                return date_of_birth
            except ValueError:
                print()
                print("La date doit être saisie au format jj/mm/aaaa")

    def _create_player(self):
        first_name = self._ask_first_name()
        last_name = self._ask_last_name()
        gender = self._ask_gender()
        date_of_birth = self._ask_birthday()
        player = Player(first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        date_of_birth=date_of_birth)
        if player.exists():
            print("Ce joueur existe déjà.")
            return
        return player

    def _ask_save_player(self, player):
        return self.view.prompt_save_or_abort(message="Voulez-vous sauvegarder le joueur: ",
                                              subject=player.__dict__)

    def _find_player_and_player_id(self):
        first_name = self._ask_first_name()
        last_name = self._ask_last_name()
        # list of players who have the same characteristics
        players = Player.search_player(first_name=first_name,
                                       last_name=last_name)
        if len(players) == 1:
            player = players[0]
            return player.doc_id, player
        if len(players) == 0:
            print("--> ⚠️INFORMATION ⚠️: Ce joueur n'existe pas.")
            return

    def _edit_or_delete_player(self):
        while True:
            choice = self.view.prompt_to_edit_or_delete_player()
            if choice == "1":
                return "edit"
            elif choice == "2":
                return "delete"
            else:
                print()
                print("--> INFORMATION: Cette réponse n'est pas autorisé.")

    def _edit_ranking_or_delete_a_player(self):
        player_in_db = self._find_player_and_player_id()
        if player_in_db is not None:
            player_id = player_in_db[0]
            player = player_in_db[1]
            instance_player = Player(**player)
            choice = self._edit_or_delete_player()
            if choice == "edit":
                new_ranking = self.view.prompt_to_change_score()
                print(f"New score: {new_ranking}")
                instance_player.update_a_ranking(new_ranking=new_ranking, player_id=player_id)
                print("Correctement mis à jour")
                return
            if choice == "delete":
                instance_player.delete_a_player(player_id=player_id)
                print("Correctement supprimé")
                return
            return

    def players_manager(self):
        players_manager_run = True
        while players_manager_run:
            choice = self._check_ask_create_player_or_upload_score()
            if choice == "off":
                print("Au revoir")
                sys.exit()

            elif choice == "return":
                print("---- RETOUR EN ARRIERE ----")
                return

            elif choice == "1":
                print("-" * 50)
                print("Création d'un joueur")
                player = self._create_player()
                if player is not None:
                    if self._ask_save_player(player=player):
                        player.save()

            elif choice == "2":
                print("-" * 50)
                print("----MISE A JOUR----")
                self._edit_ranking_or_delete_a_player()


if __name__ == "__main__":
    from views.player import PlayerView

    player_manager = PlayerView()
    player_control = Controller(view=player_manager)
    player_control.players_manager()
