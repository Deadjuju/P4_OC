"""Base view."""


class View:
    """ common views """

    CURSOR = "\n----->  || "

    @classmethod
    def information(cls, message: str):
        """
        layout of informative messages
        :param message:
        """
        print(f" ℹ️{'-' * 15} Information {'-' * 15} ℹ️\n"
              f"      ||| {message} |||\n")

    @classmethod
    def warning(cls, message):
        """
        layout of warning messages
        :param message:
        """

        print(f" ⚠️{'-' * 15} Attention {'-' * 15} ⚠️\n"
              f"      ||| {message} |||\n")

    @classmethod
    def prompt_yes_or_no(cls) -> str:
        """Prompt Yes or No"""
        return input(f"Y/n{View.CURSOR}")

    @classmethod
    def ask_question(cls, question):
        """Ask a question to user"""
        return input(question)
