# Weiss Schwarz Cancel Predictor for Android

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from random import shuffle
import operator

class CancelChance(Widget):
	chance = StringProperty()
	min_dmg = StringProperty()
	add = NumericProperty(0)

	def simulate(self, deck, damage, cancel_burns):
		damage_taken = 0
		deck_index = 0
		additional_burns = []
		for i, d in enumerate(damage):
			cancelled = False
			for _ in range(int(d)):
				if not cancelled:
					if deck[deck_index] == "CX":
						cancelled = True
						if len(cancel_burns) > i:
							additional_burns.append(cancel_burns[i].split("."))
					deck_index += 1
			if not cancelled:
				damage_taken += int(d)
		if additional_burns != [['']]:
			for burns in additional_burns:
				for d in burns:
					cancelled = False
					for _ in range(int(d)):
						if not cancelled:
							if deck[deck_index] == "CX":
								cancelled = True
							deck_index += 1
					if not cancelled:
						damage_taken += int(d)
		return damage_taken

	def calculate_all(self):
		deck_cxs = int(self.deck_cxs.text)
		deck_non_cxs = int(self.deck_cards.text) - int(self.deck_cxs.text)
		deck = []
		for _ in range(deck_cxs):
			deck.append("CX")
		for _ in range(deck_non_cxs):
			deck.append("N")
		damage = (self.damage.text).split(" ")
		cancel_burns = (self.cancel_burns.text).split(" ")
		trials = 0
		damage_prob = {}

		trials = 10000

		for _ in range(trials):
			shuffle(deck)
			damage_taken = self.simulate(deck, damage, cancel_burns)
			damage_prob[int(damage_taken)] = damage_prob.get(int(damage_taken), 0) + 1

		self.chance = "".join(["{0} damage: {1}%\n".format(x[0], round((100.0 * x[1] / trials), 4)) \
			for x in sorted(damage_prob.items(), key=operator.itemgetter(1), reverse=True)])

		self.add = len(damage_prob) * 25

		self.min_dmg = "".join(["{0}+ damage: {1}%\n".format(x[0], \
			round((100.0 * sum([v[1] for v in sorted(damage_prob.items())[i:]]) / trials), 4)) \
			for i, x in enumerate(sorted(damage_prob.items()))])

class WeissApp(App):
	def build(self):
		probability = CancelChance()
		return probability

if __name__ == '__main__':
	WeissApp().run()
