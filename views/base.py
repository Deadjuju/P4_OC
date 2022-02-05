"""Base view."""


class View:

    CURSOR = "\n----->  || "

    @classmethod
    def information(cls, message):
        print(f" ℹ️{'-' * 15} Information {'-' * 15} ℹ️\n"
              f"      ||| {message} |||\n")

    @classmethod
    def warning(cls, message):
        print(f" ⚠️{'-' * 15} Attention {'-' * 15} ⚠️\n"
              f"      ||| {message} |||\n")

    @classmethod
    def prompt_yes_or_no(cls):
        """Prompt Yes or No"""
        return input(f"Y/n{View.CURSOR}")

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


