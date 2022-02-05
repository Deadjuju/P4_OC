import datetime


from initialisation import DATE_FORMAT


class Controller:

    def __init__(self, view):
        self.view = view

    def _ask_and_check_field(self, field, message) -> str:
        """Ask and control of a field

                Returns:
                    user_choice (str): the field value
                """

        while True:
            user_choice = field()
            if user_choice != "":
                return user_choice
            else:
                self.view.warning(message=message)

    def _ask_and_check_field_date(self, field) -> str:
        """Ask and control of a date field

                Returns:
                    user_choice (str): the field value
                """

        while True:
            user_choice = field()
            try:
                datetime.datetime.strptime(user_choice, DATE_FORMAT[0])
                return user_choice
            except ValueError:
                self.view.warning(message=f"La date doit être saisie au format {DATE_FORMAT[1]}.")

    def check_yes_or_no(self, message, subject):
        print(message)
        print(subject)
        response = self.view.prompt_yes_or_no().lower()
        if response == "y" or response == "yes" or response == "oui" or response == "o":
            print("--- SAUVEGARDE ---")
            return True
        else:
            print("--- ABANDONS ---")
            return False

