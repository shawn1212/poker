# coding: utf-8

class Card:
	suits = { 'SPADES' : '♠︎', 'DIAMONDS' : '♦︎', 'HEARTS' : '♥︎', 'CLUBS' : '♣︎' }
		
	def __init__(self, value=None, suit=None):
		self.value = value
		self.suit = suit

	def suited(self, other):
		assert isinstance(other, Card), '%s is not a card' % other
		if self.suit is None or other.suit is None:
			return True
		return self.suit == other.suit
	
	def connected(self, other):
		assert isinstance(other, Card), '%s is not a card' % other
		if self.value is None or other.value is None:
			return True
		return abs(int(self) - int(other)) == 1

	def __str__(self):
		return (str(self.value) if self.value else '★') + (self.suits[self.suit] if self.suit else '★')
	def __int__(self):
		if self.value is None:
			return 0
		return Deck.values.index(self.value)
	def __float__(self):
		return int(self) / float(len(Deck.values)) 
	def __repr__(self):
		return str(self)
		return "Card('" + self.value + "', " + (("'" + self.suit + "'") if self.suit else 'None') + ")"
	def __eq__(a, b):
		if a is None and b is None:
			return True
		if a is None or b is None:
			return False
		assert isinstance(a, Card), '%s is not a card' % a
		assert isinstance(b, Card), '%s is not a card' % b
		return (a.value is None or b.value is None or a.value == b.value) and (a.suit is None or b.suit is None or a.suit == b.suit)
	def __ne__(a, b):
		return not a == b
	def __lt__(a, b):
		if a is None and b is None:
			return False
		if a is None and b is not None:
			return True
		if a is not None and b is None:
			return False
		assert isinstance(a, Card), '%s is not a card' % a
		assert isinstance(b, Card), '%s is not a card' % b
		return int(a) < int(b)
	def __gt__(a, b):
		if a is None and b is None:
			return False
		if a is None and b is not None:
			return False
		if a is not None and b is None:
			return True
		assert isinstance(a, Card), '%s is not a card' % a
		assert isinstance(b, Card), '%s is not a card' % b
		return int(a) > int(b)
	def __le__(a, b):
		if a is None and b is None:
			return True
		if a is None and b is not None:
			return True
		if a is not None and b is None:
			return False
		assert isinstance(a, Card), '%s is not a card' % a
		assert isinstance(b, Card), '%s is not a card' % b
		return int(a) <= int(b)
	def __ge__(a, b):
		if a is None and b is None:
			return True
		if a is None and b is not None:
			return False
		if a is not None and b is None:
			return True
		assert isinstance(a, Card), '%s is not a card' % a
		assert isinstance(b, Card), '%s is not a card' % b
		return int(a) >= int(b)
	def __hash__(self):
		return Deck.values.index(self.value) * 10 ** (Deck.suits.index(self.suit) if self.suit is not None else len(Deck.values))

class Deck:
	values = [str(val) for val in range(2, 11) + list('JQKA')]
	suits = ['SPADES', 'HEARTS', 'CLUBS', 'DIAMONDS']
	chunks = [values[start:start+5] for start in xrange(0, len(values) - 5 + 1)]

	def __init__(self, hand=None):
		self.cards = [Card(value, suit) for value in self.values for suit in self.suits]
		if hand:
			self.cards = [found for found in self.cards if found not in [card for card in hand if card.value is not None]]

	def __len__(self):
		return len(self.cards)

	def __getitem__(self, position):
		return self.cards[position]

	def __setitem__(self, key, val):
		self.cards[key] = val

	def __str__(self):
		return str(list(self))

	def deal(self, n=1):
		return [self.cards.pop() for i in range(0,n)]

	def peek(self, value=None, suit=None, card=None):
		if card is not None:
			value = card.value
			suit = card.suit
		return [found for found in self.cards if (value is None or found.value == value) and (suit is None or found.suit == suit)]

	def draw(self, value=None, suit=None):
		cards = self.peek(value, suit)
		for card in cards:
			self.cards.remove(card)
		return cards