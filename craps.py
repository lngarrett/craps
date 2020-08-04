"""Craps"""
from __future__ import absolute_import
import sys
import random
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
if LOGGER.handlers:
    for log_handler in LOGGER.handlers:
        LOGGER.removeHandler(log_handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Game():
    """Craps."""

    def __init__(self, shooter):
        self.point = None
        self.shooter = shooter
        self.bets = []
        self.current_roll = None
        self.dice1_current = None
        self.dice2_current = None

    def come_out(self, roll):
        """Set the point."""

        if not self.point and roll not in [2, 3, 7, 11, 12]:
            self.point = roll
            LOGGER.info("The point is %s", roll)
        elif self.point:
            raise Exception('Point was already set.')

    def roll_dice(self):
        """Hands high let 'em fly."""

        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.dice1_current = dice1
        self.dice2_current = dice2
        self.current_roll = dice1 + dice2

        LOGGER.info(
            'Shooter %s rolls a %s, %s for a %s', 
            self.shooter,
            self.dice1_current,
            self.dice2_current,
            self.current_roll
        )

        self.check_bets()

        if not self.point:
            self.come_out(self.current_roll)
        elif self.point and self.current_roll == self.point:
            LOGGER.info('Point hit! %s', self.point)
        elif self.point and self.current_roll == 7:
            LOGGER.info('Seven out!')

    def place_bet(self, bet):
        """New action."""
        self.bets.append(bet)

    def check_bets(self):
        """Process bets and removed resolved bets."""
        remaining_bets = []
        for bet in self.bets:
            if not bet.resolved and bet.active:
                bet.resolve_check(self)
                if not bet.resolved:
                    remaining_bets.append(bet)
        self.bets = remaining_bets



class Bet():
    """A bet."""
    pays = 1

    def __init__(self, bettor, amount):
        self.bettor = bettor
        self.amount = amount
        self.resolution_amount = None
        self.won = None
        self.resolved = False
        self.active = True

    def resolve_check(self, _game):
        """Fuck it, free money."""
        return self.win()

    def win(self):
        """Process a win."""
        self.won = True
        self.resolved = True
        self.resolution_amount = self.amount + self.amount * Bet.pays
        LOGGER.info(
            'Bettor %s won a %s %s bet! Pays %s',
            self.bettor,
            self.amount,
            self.__class__.__name__,
            self.resolution_amount
        )

    def lose(self):
        """Process a loss."""
        self.won = False
        self.resolved = True
        self.resolution_amount = 0
        LOGGER.info(
            'Bettor %s lost a %s %s bet!',
            self.bettor,
            self.amount,
            self.__class__.__name__
        )

class PassLine(Bet):
    """Pass line."""
    pays = 1

    def resolve_check(self, game):
        if not game.point and game.current_roll in [7, 11]:
            self.win()
        elif not game.point and game.current_roll in [2, 3, 12]:
            self.lose()
        elif game.point and game.current_roll == game.point:
            self.win()
        elif game.point and game.current_roll == 7:
            self.lose()
        else:
            LOGGER.info(
                'Bettor %s %s %s bet stands.',
                self.bettor,
                self.amount,
                self.__class__.__name__
            )