import random, linecache
from collections import Counter
import sqlite3
from prettytable import PrettyTable

class Game():

    def __init__(self, name):
        self.player_name = name
        self.player_score = 0
        self._generate = random.randint(1, 801)
        self._secret_word = linecache.getline('movies.txt', self._generate)[:-1]
        self.dashes = "_" * len(self._secret_word)
        Game.secret_exception(self,self._secret_word)
        self.guesses_left = 6
        self.wrong_count = 0
        self.correct_cnt = 0
        self.letter_storage = []

    def secret_exception(self, secw):
        exaplhabet = ["-","'","(",")","/",":","!","?",'"',",","&","."," "]
        for i in range(len(exaplhabet)):
            if exaplhabet[i] in secw:
                self.dashes = Game.update_dashes(self,self._secret_word, self.dashes, exaplhabet[i])
        
    def update_dashes(self, secret, cur_dash, rec_guess):
        self.result = ""

        for i in range(len(secret)):
            if secret[i].lower() == rec_guess.lower():
                self.result = self.result + rec_guess # Adds guess to string if guess is correctly

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
        return guess.lower() == self._secret_word.lower()

    def get_dashes(self):
        return Counter(self.dashes)["_"]

    def is_whole(self, guess):
        if  Game.is_wholeword(self, guess) and (Game.get_dashes(self) >= len(self._secret_word)//2):
            self.player_score = len(self._secret_word)
            return 'we'
        elif Game.is_wholeword(self, guess):
            self.correct_cnt = len(Counter(self._secret_word).keys())
            return 'w'
        else:
            return 'single'

    def update_score(self, p_name, p_score):
        # db connect
        conn = sqlite3.connect('scores.db')
        # add record
        conn.execute("INSERT INTO Scoreboard (Name,Score) \
             	        VALUES (?, ?)", (p_name,p_score))
        conn.commit()

        conn.close()

    # ptable from https://pypi.org/project/PrettyTable
    def show_scoreboard(self):
        conn = sqlite3.connect('scores.db')
        # query
        t = PrettyTable(['Name', 'Score'])
        cursor = conn.execute("SELECT Name, Score FROM Scoreboard ORDER BY Score DESC LIMIT 5")
        for row in cursor:
            t.add_row([row[0], row[1]])
        return t.get_string()

        conn.close()

    def check_guess(self, guess):
        # the guess is in the secret word
        if len(guess) == 1 and guess.lower() in self._secret_word.lower():
            self.correct_cnt += 1
            self.in_secret = 1
            # update dash
            self.dashes = Game.update_dashes(self,self._secret_word, self.dashes, guess)
            # update score
            self.player_score += 1
        else:
            self.wrong_count += 1
            self.guesses_left -= 1
            self.in_secret = 0
        # add guessed letter to letter_storage list
        if len(guess) == 1: Game.check_letter(self, guess)
        return self.in_secret