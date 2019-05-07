import random
from collections import Counter
import linecache

class Game():

    def __init__(self,name):
        self.player_name = name
        self.player_score = 0
        self._generate = random.randint(1, 734)
        self._secret_word = linecache.getline('words.txt', self._generate)[:-1]
        self.dashes = "-" * len(self._secret_word)
        self.guesses_left = 6
        self.wrong_count = 0
        self.correct_cnt = 0
        self.letter_storage = []
        
    def update_dashes(self,secret, cur_dash, rec_guess):
        self.result = ""

        for i in range(len(secret)):
            if self.secret[i] == self.rec_guess:
                self.result = self.result + self.rec_guess # Adds guess to string if guess is correctly

            else:
                # Add the dash at index i to result if it doesn't match the guess
                self.result = self.result + cur_dash[i]
    
        return self.result

    def reset(self):
        self.__init__(self.player_name)