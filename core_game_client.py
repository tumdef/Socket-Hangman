
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

     def check_letter(self, isinserver, guess):
        if isinserver == 1:
            self.letter_storage.append(guess)
        else:
             print("Sorry, you're already guessed this letter!")

     def __init__(self):
          self.wrong_count = 0
          self.letter_storage = []
          print("{}\n".format(self._hangman[0]))

     def reset(self):
          self.__init__()

     def chk_ans_type(self, ans_type):
          if ans_type == "we":
               print("Congrats! You win. You just guessed the whole word and get extra score!")
          elif ans_type == "w":
               print("Congrats! You win. You just guessed the whole word! but did not get extra score :(")