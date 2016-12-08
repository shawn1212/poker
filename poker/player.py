from poker.hand import Hand
from random import uniform, randint

class RNN:
	def __init__(self):
		pass

	def step(self, inputs):
		return uniform(-1, 1)

class Player:
	def __init__(self, name, cards, stack_size, seed_bet):
		self.name = str(name)
		self.reset(cards)
		self.stack = stack_size
		self.folded = False
		self.rnn = RNN()
		self.base_bet = seed_bet

	def reset(self, cards):
		self.pocket = Hand(cards)
		self.hand = self.pocket

	def set_board(self, board):
		self.hand = self.pocket + board

	def act(self, board, position, players, bet, pot):
		assert not self.folded, 'Folded player should not be in the hand.'

		# Normalize the position
		position = float(position) / float(len(players))

		# Normalize the number of players in the hand
		remaining = len([player for player in players if not player.folded])
		remaining = float(remaining) / float(len(players))

		# Normalize pot odds 
		pot_odds = float(bet) / float(pot) if pot > 0 else 0

		# Normalize stack ratio
		stack_ratio = float(bet) / float(self.stack) if self.stack > 0 else 0

		# Build the inputs tuple
		inputs = (position, remaining, pot_odds, stack_ratio) 
		inputs += tuple(float(card) for card in self.hand) 
		inputs += tuple(0 for i in xrange(0, max(0, 7 - len(self.hand))))

		# Feed the RNN
		outcome = self.rnn.step(inputs)

		return self.calculate_bet(outcome, bet, pot)

	def bet(self, bet):
		bet = min(self.stack, bet)
		self.stack -= bet
		return bet

	def calculate_bet(self, outcome, to_call, pot):
		delta = 0.25
		bet = 0
		if outcome > 3 * delta:
			bet = pot if pot else self.base_bet * 3
		elif outcome > 2 * delta:
			bet = int(pot / 2) if pot else self.base_bet * 3
		elif outcome > delta:
			bet = int(to_call * 2) if to_call else self.base_bet
		elif outcome > -2 * delta and outcome < delta:
			bet = to_call
		elif outcome < -3 * delta:
			bet = 0
			if to_call > 0:
				self.folded = True

		return self.bet(bet)

	def __len__(self):
		return self.stack

	def __str__(self):
		return "[" + self.name + " : " + str(self.pocket) + ", Chips: " + str(self.stack) + ", Best: " + str(self.hand.best()) + (", FOLDED" if self.folded else "") + "]" 

	def __lt__(self, other):
		if self.folded:
			return True
		if other.folded:
			return False
		return self.hand.best() < other.hand.best()

	def __gt__(self, other):
		if self.folded:
			return False
		if other.folded:
			return True
		return self.hand.best() > other.hand.best()

	def __le__(self, other):
		if self.folded and other.folded:
			return True
		if self.folded:
			return True
		if other.folded:
			return False
		return self.hand.best() <= other.hand.best()

	def __ge__(self, other):
		if self.folded and other.folded:
			return True
		if self.folded:
			return False
		if other.folded:
			return True
		return self.hand.best() >= other.hand.best()

	def __eq__(self, other):
		if self.folded and other.folded:
			return True
		if self.folded or other.folded:
			return False
		return self.hand.best() == other.hand.best()

	def __ne__(self, other):
		if self.folded and other.folded:
			return False
		if self.folded or other.folded:
			return True
		return self.hand.best() != other.hand.best()