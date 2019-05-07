import random
from collections import Counter
import linecache

class Game():

    def __init__(self, name):
        self.player_name = name
        self.player_score = 0
        self._generate = random.randint(1, 734)
        self._secret_word = linecache.getline('words.txt', self._generate)[:-1]
        self.dashes = "-" * len(self._secret_word)
        self.guesses_left = 6
        self.wrong_count = 0
        self.correct_cnt = 0
        self.letter_storage = []
        
    def update_dashes(self, secret, cur_dash, rec_guess):
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

    def check_letter(self, guess):
        if guess not in self.letter_storage:
            self.letter_storage.append(guess)
            return 1
        return 0
    
    def is_wholeword(self, guess):
        return guess == self._secret_word

    def get_dashes(self):
        return Counter(self.dashes)["-"]

    def check_guess(self, guess):
        if  Game.is_wholeword(self, guess) and (Game.get_dashes(self) > len(self._secret_word)//2):
            self.player_score =  len(self._secret_word)
            return 'we'
        elif Game.is_wholeword(self, guess):
            self.correct_cnt = len(Counter(self._secret_word).keys())
            return 'w'
        else:
            return '0'