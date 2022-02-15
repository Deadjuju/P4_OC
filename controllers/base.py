import datetime
from typing import Tuple

from initialisation import DATE_FORMAT


class Controller:
    """Implement other controllers"""

    def __init__(self, view):
        self.view = view

    def _ask_and_check_field(self, field, message: str) -> str:
        """Ask and control of a field
                Args:
                    field (): Method to get the value of a field
                    message (str): Message in case of warning
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
                Args:
                    field (): Method to get the value of a field
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

    def check_yes_or_no(self, message: str, subject, commit_message: Tuple[str]) -> bool:
        """Ask and control a confirmation for an action
                Args:
                    message (str): Confirmation message
                    subject (): Subject concerned by the confirmation
                    commit_message (Tuple[str]): Message that displays the decision
                Returns:
                    (bool)
                """

        print(message)
        print(subject)
        response = self.view.prompt_yes_or_no().lower()
        if response == "y" or response == "yes" or response == "oui" or response == "o":
            print(commit_message[0])
            return True
        else:
            print(commit_message[1])
            return False

    def control_list_of_user_choices(self, responses_list: dict, question: str, message: str) -> str:
        """Ask and control response with a list of proposition
                Args:
                    responses_list (dict): list of responses and return value
                    question (str): Subject concerned by the confirmation
                    message (str): Message in case of warning
                Returns:
                    (str): response
                """

        while True:
            choice = self.view.ask_question(question=question)
            if responses_list.get(choice) is not None:
                return responses_list.get(choice)
            else:
                self.view.warning(message=message)

