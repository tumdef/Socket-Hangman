
class Game():
    _hangman = (
        """
             _____
             |  \|
                 |
                 |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
                 |
                 |
                 |
            =========""",

        """
             _____
             |  \|
             O   |
             |   |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
             |\  |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
                 |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
              \  |
                 |
            =========""",
        """
             _____
             |  \|
             O   |
            /|\  |
            / \  |
                 |
            =========""")

    def __init__(self):
        wrong_count = 0
        print("{}\n".format(self._hangman[0]))