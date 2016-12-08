from poker.deck import Deck
from poker.hand import Hand
from poker.player import Player
from random import shuffle
from collections import deque
from time import sleep

class Game:
	BIG_BLIND = 100
	def __init__(self, players=5):
		self.num_players = players
		self.players = None
		self.deck = Deck()
		self.pot = 0

	def play(self):
		try:
			while True:
				self.deal()
				board = Hand([])
				self.action(board, preflop=True)
				board += self.flop()
				self.action(board)
				board += self.turn()
				self.action(board)
				board += self.river()
				self.action(board)
				self.winner()
				if len(raw_input('Press enter to play again, enter any text and press enter to stop.').strip()) > 0:
					break
		except KeyboardInterrupt:
			print "Done!"

	def set_board(self, board):
		for player in self.players:
			if not player.folded:
				player.set_board(board)

	def action(self, board, preflop=False):
		print "\nACTION"
		print "------"
		print "BOARD: " + str(board)

		self.set_board(board)

		players = enumerate(self.players)
		bet = 0
		to_call = 0

		for position, player in players:
			print "[+] Player: " + str(player)
			if preflop and position == 0:
				print "[-] Small Blind"
				bet = player.bet(int(Game.BIG_BLIND / 2))
				to_call = int(Game.BIG_BLIND / 2)
			elif preflop and position == 1:
				print "[-] Big Blind"
				bet = player.bet(Game.BIG_BLIND)
				to_call = Game.BIG_BLIND
			elif not player.folded:
				bet = player.act(board, position, self.players, to_call, self.pot)
				if player.folded:
					print "[-] Fold"
				elif bet == 0:
					print "[-] Check"
				elif bet == to_call:
					print "[-] Call: " + str(bet)
				else:
					print "[-] Bet: " + str(bet)
					to_call = bet
			else:
				print "[-] Folded"

			self.pot += bet

	def winner(self):
		print "\nRESULTS"
		print "-------"
		winner = max(self.players)
		winners = [player for player in self.players if player.hand.best() == winner.hand.best()]

		print "\nWINNERS"
		for winner in winners:
			winner.stack += int(self.pot / len(winners))
			print winner
		self.pot = 0

	def deal(self):
		print "\nNEW HAND"
		print "--------"
		self.deck = Deck()
		shuffle(self.deck)
		if self.players is None:
			self.players = deque([Player('Player ' + str(i), self.deck.deal(2), 100000, Game.BIG_BLIND) for i in xrange(0, self.num_players)])
		else:
			self.players.rotate(1)
			for player in self.players:
				if bool(player):
					player.reset(self.deck.deal(2))
					player.folded = False
				else:
					player.reset([])


	def flop(self):
		self.deck.deal(1) #burn
		return self.deck.deal(3)

	def turn(self):
		self.deck.deal(1) #burn
		return self.deck.deal(1)

	def river(self):
		self.deck.deal(1) #burn
		return self.deck.deal(1)
