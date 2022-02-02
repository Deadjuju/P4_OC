import datetime
import sys

from models.person import Player


class Controller:

    def __init__(self, view):
        self.view = view

    def _check_ask_create_player_or_upload_ranking(self):
        while True:
            choice = self.view.ask_create_player_or_upload_ranking()
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
                        date_of_birth=date_of_birth,
                        ranking=1)
        if player.exists():
            print("Ce joueur existe déjà.")
            return
        return player

    def _ask_save_player(self, player):
        return self.view.prompt_save_or_abort(message="Voulez-vous sauvegarder le joueur: ",
                                              subject=player.__dict__)

    def _find_player(self):
        first_name = self._ask_first_name()
        last_name = self._ask_last_name()
        date_of_birth = self._ask_birthday()
        player = Player.search_player(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)[0]
        print("-" * 50)
        print("Joueur trouvé:")
        print(player)
        return player

    def players_manager(self):
        players_manager_run = True
        while players_manager_run:
            choice = self._check_ask_create_player_or_upload_ranking()
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
                player = self._find_player()
                player_in_db = Player(**player)
                print(player_in_db)
                print(player_in_db.exists())


if __name__ == "__main__":
    from views.base import PlayerView
    player_manager = PlayerView()
    player_control = Controller(view=player_manager)
    player_control.players_manager()
