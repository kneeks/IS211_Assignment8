# -*- coding: utf-8 -*-
"""
Week 8 - Assignment
"""


import argparse
import time
import random


parser = argparse.ArgumentParser()
p1 = parser.add_argument('--player1', type=str, help='Choose a human or '
                                               'computer player type.')    
p2 = parser.add_argument('--player2', type=str, help='Choose a human or '
                                               'computer player type.')
parser.add_argument('--timed', help='Complete game in 60 seconds or less?')
args = parser.parse_args()


class Die(object):
    """the die which has 6 sides"""
    def __init__(self):
        self.dienum = 0

    def roll(self):
        self.dienum = random.randint(1, 6)
        return self.dienum


class Player(object):
    """constructor for the players"""
    def __init__(self, name):
        self.name = name
        self.totscore = 0
        self.turnscore = 0
        self.turn = 0
        self.type = 'Human'


class ComputerPlayer(Player):
    """constructor for computer player"""
    def __init__(self):
        Player.__init__(self, name='Computer')
        self.type = 'Computer'


class PlayerFactory(object):
    """"""
    def player_type(self, player_type, name='Player 1'):
        if player_type[0].lower() == 'h':
            return Player(name)
        elif player_type[0].lower() == 'c':
            return ComputerPlayer()


class Game(object):
    """constructor for Pig Game"""
    def __init__(self, player1, player2):  
        pigplayers = PlayerFactory()
        self.player1 = pigplayers.player_type(args.p1)
        self.player2 = pigplayers.player_type(args.p2)
        self.die = Die()
        self.turn(self.player1)
    
    def turn(self, player):
        """a players turn"""
        player.turn = 1
        print '\nit is Player {}\'s turn'.format(player.name)
        while player.turn == 1 and player.totscore < 100:           
            r = self.die.roll()
            print '\nyou rolled a {}\n'.format(r)
            if r == 1:
                player.turnscore = 0
                print ('oops! you rolled a 1, '
                       'next player.\n').format(player.name, player.totscore)
                print '-' * 60, '\n'
                self.next_player()
            else:
                player.turnscore += r
                print 'your total this turn is {}\n'.format(player.turnscore)
                self.player_ans(player)
        print ('{} is the winner '
               'with a score of {}!').format(player.name, player.totscore)
               
    def player_ans(self, player):
        """players answer to their roll"""
        if player.type == 'Computer':
            hold_var = 100 - player.totscore
            if hold_var > 25:
                hold_var = 25
            if player.turnscore >= hold_var:
                player.totscore += player.turnscore
                print ('your total this turn is '
                       '{}\n').format(player.turnscore, player.name)
                if player.totscore >= 100:
                    print ('{} is the winner '
                           'with a score of '
                           '{}!').format(player.name, player.totscore)
                    raise SystemExit
                else:
                    player.turnscore = 0
                    print ('{}\'s total score is'
                           ' now {}.\n\n').format(player.name, player.totscore)
                    print '-' * 60, '\n'
                    self.next_player()
            else:
                self.turn(player)
        ans = raw_input('would you like to roll again? '
                        'r = roll h = hold ').lower()
        if ans == 'h':
            player.totscore += player.turnscore
            print '\nyour turn is now over.\n'
            if player.totscore >= 100:
                print ('{} wins.').format(player.name, player.totscore)
            else:
                player.turnscore = 0
                print ('{}\'s total score is'
                       ' now {}.\n\n').format(player.name, player.totscore)
                print '-' * 60, '\n'
                self.next_player()
        elif ans == 'r':
            self.turn(player)
        else:
            print 'Invalid option, r = roll h = hold '
            self.player_ans(player)     
                
    def next_player(self):
        """initiates next players turn"""
        if self.player1.turn == 1:
            self.player1.turn = 0
            self.turn(self.player2)
        else:
            self.player2.turn_status = 0
            self.turn(self.player1)


class TimedGameProxy(Game):
    """timed game of pig"""
    def __init__(self):
        self.start_time = time.time()
        Game.__init__(self, 'Player1', 'Player2')

    def time_tracker(self):
        if time.time() - self.start_time >= 60:
            if self.player1.totscore > self.player2.totscore:
                print ('Time has ended! {} '
                       'wins with a score '
                       'of {}.').format(self.player1.name,
                                        self.player1.totscore)
            else:
                print ('Time has ended! {} '
                       'wins with a score '
                       'of {}.').format(self.player2.name,
                                        self.player2.totscore)
                raise SystemExit
        else:
            time_left = time.time() - self.start_time
            print ('{} seconds have passed. You may '
                   'continue playing').format(time_left)


def main():
    """initiates the program"""
    print 'welcome to pig'
    raw_input('press enter to begin rolling!')
    Game(p1, p2)


if __name__ == '__main__':
    main()