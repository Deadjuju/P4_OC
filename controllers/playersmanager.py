import datetime
import sys

from controllers.base import Controller
from models.person import Player


class PlayerController(Controller):

    def __init__(self, view):
        super().__init__(view)

    def _check_ask_create_player_or_upload_score(self) -> str:
        """User choice control which allows to select the option to execute

                Returns:
                    choice (str): the desired choice
                """
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
                self.view.warning(message="Merci de renseigner 1, 2 ou 3.")

    def _ask_gender(self) -> str:
        """Ask and control of the gender field

                Returns:
                    gender (str): gender
                """

        while True:
            gender = self.view.prompt_for_player_gender().lower()
            if gender == "femme" or gender == "female":
                return "Female"
            elif gender == "homme" or gender == "male":
                return "Male"
            else:
                self.view.warning(message="Merci de renseigner un genre valide.")

    def _ask_birthday(self) -> str:
        """Returns the date_of_birth (str)"""
        birth_date = self.view.prompt_for_player_date_of_birth
        return self._ask_and_check_field_date(field=birth_date)

    def _create_player(self) -> Player:
        """Create an instance of Player

                Returns:
                    first_name (str): first name
                """

        first_name = self._ask_and_check_field(field=self.view.prompt_for_player_first_name,
                                               message="Le champ - prénom - ne peut pas être vide.").title()
        last_name = self._ask_and_check_field(field=self.view.prompt_for_player_last_name,
                                              message="Le champ - nom - ne peut pas être vide.").title()
        gender = self._ask_gender()
        date_of_birth = self._ask_birthday()
        player = Player(first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        date_of_birth=date_of_birth)
        return player

    def _find_players_list(self) -> list:
        """Find in database the list of players who have the same characteristics

                Returns:
                    (list): list of players
                """

        first_name = self._ask_and_check_field(field=self.view.prompt_for_player_first_name,
                                               message="Le champ - prénom - ne peut pas être vide.").title()
        last_name = self._ask_and_check_field(field=self.view.prompt_for_player_last_name,
                                              message="Le champ - nom - ne peut pas être vide.").title()

        # list of players who have the same characteristics
        players = Player.search_player(first_name=first_name,
                                       last_name=last_name)
        return players

    def _edit_or_delete_player(self) -> str:
        """Ask and control user choice: edit a player or delete it

                Returns:
                    (str): user choice
                """

        while True:
            choice = self.view.prompt_to_edit_or_delete_player()
            if choice == "1":
                return "edit"
            elif choice == "2":
                return "delete"
            else:
                self.view.information(message="Cette réponse n'est pas autorisé.")

                print()
                print("")

    def _edit_ranking_or_delete_a_player(self, player):
        """Make action to edit a player or to delete it

                Args:
                    player (): BeautifulSoup object pointing to the table of characteristics
                """

        player_id = player.doc_id
        instance_player = Player(**player)
        choice = self._edit_or_delete_player()
        if choice == "edit":
            new_ranking = self.view.prompt_to_change_score()
            print(f"New score: {new_ranking}")
            instance_player.update_a_ranking(new_ranking=new_ranking, player_id=player_id)
            self.view.print_the_edit_delete_choice(choice=choice)
            return
        if choice == "delete":
            instance_player.delete_a_player(player_id=player_id)
            return

    def players_manager(self):
        """execution and selection of the different choices"""
        players_manager_run = True
        while players_manager_run:
            choice = self._check_ask_create_player_or_upload_score()
            if choice == "off":
                self.view.information(message="A BIENTOT!!!")
                sys.exit()

            elif choice == "return":
                self.view.information(message="---- RETOUR EN ARRIERE ----")
                return

            elif choice == "1":
                self.view.information(message="Création d'un joueur: ")
                player = self._create_player()
                if not player.exists():
                    if self.check_yes_or_no(message="Voulez-vous sauvegarder le joueur: ",
                                            subject=player.__dict__):
                        player.save()
                else:
                    self.view.warning(message="Ce joueur existe déjà.")

            elif choice == "2":
                self.view.warning(message="---- MISE A JOUR JOUEUR----")
                players_list = self._find_players_list()
                if len(players_list) == 1:
                    player = players_list[0]
                    self.view.show_the_player_found(player=True)
                    self._edit_ranking_or_delete_a_player(player=player)
                if len(players_list) == 0:
                    self.view.show_the_player_found(player=False)


if __name__ == "__main__":
    from views.player import PlayerView

    player_manager = PlayerView()
    player_control = PlayerController(view=player_manager)
    player_control.players_manager()
