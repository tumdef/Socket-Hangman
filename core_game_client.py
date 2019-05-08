
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
          if isinserver:
               if len(guess) == 1:
                    self.letter_storage.append(guess)
               return 0
          elif len(guess) == 1:
               print("Sorry, you're already guessed this letter!")
          return 1

     def __init__(self):
          self.wrong_count = 0
          self.letter_storage = []

     def reset(self):
          self.__init__()

     def chk_ans_type(self, ans_type):
          if ans_type == "we" or ans_type == "w":
               return 1
          return 0

     def check_guess(self, is_in_secret, guess):
          if is_in_secret:
               print("The letter '{}' is in the secret word!".format(guess))
          else:
               print("The letter '{}' is not in the secret word!".format(guess))