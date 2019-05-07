import random, linecache
from collections import Counter
import sqlite3
from prettytable import PrettyTable

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
        if Game.is_wholeword(self, guess) and (Game.get_dashes(self) > len(self._secret_word)//2):
            print("Congrats! You win. You just guessed the whole word and get extra score!")
            self.player_score =  len(self._secret_word)
        else:
            pass

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
        cursor = conn.execute("SELECT Name, Score FROM Scoreboard ORDER BY Score DESC")
        for row in cursor:
            t.add_row([row[0], row[1]])
        print (t)

        conn.close()