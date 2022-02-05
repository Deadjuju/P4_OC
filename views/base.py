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


