from poker.deck import Deck, Card
from collections import defaultdict
from itertools import combinations, chain
import pprint

class Hand:
	order = ['straight_flush', 'four_of_a_kind', 'full_house', 'flush', 'straight', 'three_of_a_kind', 'two_pair', 'pair']

	def __init__(self, cards):
		self.cards = sorted(list(cards))
		self.matches = self._matches()
		self.counts = self._counts()

	def _matches(self):
		matches = defaultdict(list)
		for card in self.cards:
			if card.value is not None:
				matches[card.value].append(card)
		return matches

	def _counts(self):
		counts = { i : [] for i in xrange(1,6) }
		for match in self.matches:
			counts[len(self.matches[match])].append(Card(match, None))
		return counts

	def best(self):
		if len(self.cards) > 5:
			return max([FiveCardHand(combination) for combination in combinations(self.cards, 5)])
		elif len(self.cards) == 5:
			return FiveCardHand(self.cards)

	def connected(self, prev, curr):
		return curr if prev is not None and prev.connected(curr) else None

	def suited(self, prev, curr):
		return curr if prev is not None and prev.suited(curr) else None

	def weight(self):
		start = 0
		for card in self.cards:
			start += len(Deck.values) ** int(card)
		return start

	def __add__(self, other):
		if isinstance(other, Card):
			cards = self.cards
			cards.append(other)
		elif isinstance(other, list):
			cards = self.cards + other
		elif isinstance(other, Hand):
			cards = self.cards + other.cards
		else:
			raise Exception("Invalid card type")

		return Hand(cards)

	def __radd__(self, other):
		if isinstance(other, Card):
			cards = self.cards
			cards.append(other)
		elif isinstance(other, list):
			cards = self.cards + other
		elif isinstance(other, Hand):
			cards = self.cards + other.cards
		else: 
			raise Exception("Invalid card type")
			
		return Hand(cards)

	def __sub__(self, other):
		if isinstance(other, Card):
			cards = [card for card in self.cards if card != other]
		elif isinstance(other, list):
			cards = [card for card in self.cards if card not in other]
		elif isinstance(other, Hand):
			cards = [card for card in self.cards if card not in other.cards]
		else:
			raise Exception("Invalid card type")

		return Hand(cards)

	def __rsub__(self, other):
		if isinstance(other, Card):
			cards = [card for card in self.cards if card != other]
		elif isinstance(other, list):
			cards = [card for card in self.cards if card not in other]
		elif isinstance(other, Hand):
			cards = [card for card in self.cards if card not in other.cards]
		else:
			raise Exception("Invalid card type")

		return Hand(cards)

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return "(" + " ".join(map(str,self.cards)) + ")"

	def __len__(self):
		return len(self.cards)

	def __getitem__(self, position):
		return self.cards[position]

	def __setitem__(self, key, val):
		self.cards[key] = val

	def __gt__(a, b):
		if a is None and b is None:
			return False
		if a is None and b is not None:
			return True
		if a is not None and b is None:
			return False
		return a.best() > b.best()

	def __lt__(a, b):
		if a is None and b is None:
			return False
		if a is None and b is not None:
			return True
		if a is not None and b is None:
			return False
		return a.best() < b.best()

	def __le__(a, b):
		if a is None and b is None:
			return True
		if a is None and b is not None:
			return True
		if a is not None and b is None:
			return False
		return a.best() <= b.best()

	def __ge__(a, b):
		if a is None and b is None:
			return True
		if a is None and b is not None:
			return False
		if a is not None and b is None:
			return True
		return a.best() >= b.best()

class FiveCardHand(Hand):
	def __init__(self, cards):
		assert len(cards) == 5, "A hand must have exactly 5 cards"
		Hand.__init__(self, cards)

	def results(self):
		return {
			'straight_flush' : self.straight_flush(),
			'four_of_a_kind' : self.four_of_a_kind(),
			'full_house' : self.full_house(),
			'flush' : self.flush(),
			'straight' : self.straight(),
			'three_of_a_kind' : self.three_of_a_kind(),
			'two_pair' : self.two_pair(),
			'pair' : self.pair(),
			'weight' : self.weight()
		}

	def strongest(self):
		results = self.results()
		for hand in Hand.order:
			if results[hand]:
				return hand

	def pair(self):
		return max(self.counts[2]) if len(self.counts[2]) else None

	def two_pair(self):
		if len(self.counts[2]) >= 2:
			return sorted(self.counts[2])[0:2]

	def three_of_a_kind(self):
		if len(self.counts[3]):
			return max(self.counts[3])

	def straight(self):
		return max(self.cards) if reduce(self.connected, self.cards) is not None else None

	def flush(self):
		return max(self.cards) if reduce(self.suited, self.cards) is not None else None

	def full_house(self):
		if len(self.counts[3]) == 2:
			return tuple(sorted(self.counts[3])[0:2])
		if len(self.counts[3]) == 1 and len(self.counts[2]) >= 1:
			return (max(self.counts[3]), max(self.counts[2])) 
		if len(self.counts[4]) == 1 and len(self.counts[2]) >= 1:
			return (max(self.counts[4]), max(self.counts[2]))
		if len(self.counts[4]) == 1 and len(self.counts[3]) == 1:
			return (max(self.counts[4]), max(self.counts[3]))

	def four_of_a_kind(self):
		return max(self.counts[4]) if len(self.counts[4]) else None

	def straight_flush(self):
		return max(self.cards) if reduce(self.suited, self.cards) is not None and reduce(self.connected, self.cards) is not None else None

	def __eq__(left, right):
		if left is None and right is None:
			return True
		if left is None:
			return False
		if right is None:
			return False
		return left.strongest() == right.strongest() and left.weight() == right.weight()

	def __gt__(left, right):
		if left is None and right is None:
			return False
		if left is None:
			return False
		if right is None:
			return True
		return right.beats(left)

	def __ge__(left, right):
		if left is None and right is None:
			return True
		if left is None:
			return False
		if right is None:
			return True
		return right == left or right.beats(left)

	def __lt__(left, right):
		if left is None and right is None:
			return False
		if left is None:
			return True
		if right is None:
			return False

		return left.beats(right)

	def __le__(left, right):
		if left is None and right is None:
			return True
		if left is None:
			return True
		if right is None:
			return False

		return left == right or left.beats(right)

	def beats(self, other):
		a = self.results()
		b = other.results()
		# print a
		# print b

		if a['straight_flush'] or b['straight_flush']:
			return a['straight_flush'] < b['straight_flush']
			
		if a['four_of_a_kind'] or b['four_of_a_kind']:
			if a['four_of_a_kind'] == b['four_of_a_kind']:
				return a['weight'] < b['weight']
			return a['four_of_a_kind'] < b['four_of_a_kind']
			
		if a['full_house'] and b['full_house']:
			if a['full_house'][1] == b['full_house'][1]:
				return a['full_house'][0] < b['full_house'][0]
			return a['full_house'][1] < b['full_house'][1]
		elif a['full_house']:
			return False
		elif b['full_house']:
			return True

		if a['flush'] or b['flush']:
			if a['flush'] == b['flush']:
				return a['weight'] < b['weight']
			return a['flush'] < b['flush']
			
		if a['straight'] or b['straight']:
			if a['straight'] == b['straight']:
				return a['weight'] < b['weight']
			return a['straight'] < b['straight']
			
		if a['three_of_a_kind'] or b['three_of_a_kind']:
			if a['three_of_a_kind'] == b['three_of_a_kind']:
				return a['weight'] < b['weight']
			return a['three_of_a_kind'] < b['three_of_a_kind']
			
		if a['two_pair'] or b['two_pair']:
			if a['two_pair'] and b['two_pair']:
				if a['two_pair'][1] == b['two_pair'][1]:
					if a['two_pair'][0] == b['two_pair'][0]:
						return a['weight'] < b['weight']
					return a['two_pair'][0] < b['two_pair'][0]
				return a['two_pair'][1] < b['two_pair'][1]
			elif a['two_pair']:
				return False
			else:
				return True

		if a['pair'] or b['pair']:
			if a['pair'] and b['pair']:
				if a['pair'] == b['pair']:
					return a['weight'] < b['weight']
				return a['pair'] < b['pair']
			elif a['pair']:
				return False
			else:
				return True
		
		return a['weight'] < b['weight']