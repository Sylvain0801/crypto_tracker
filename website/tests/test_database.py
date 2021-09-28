import unittest
from website.models import Money, Evolution


class DatabaseInsertTests(unittest.TestCase):
	def setUp(self):
		self.money = Money(name='Fantom', value='1.11', quantity='842.0')
		self.evolution = Evolution(value='173.03743569286')

	def test_add_money_equal(self):
		self.assertEqual(self.money.name, 'Fantom')
		self.assertEqual(self.money.value, '1.11')
		self.assertEqual(self.money.quantity, '842.0')

	def test_add_money_false(self):
		self.assertFalse(self.money.name == 'Fantoms')
		self.assertFalse(self.money.value == '1')
		self.assertFalse(self.money.quantity == '842')
	
	def test_add_evolution_equal(self):
		self.assertEqual(self.evolution.value, '173.03743569286')

	def test_add_evolution_false(self):
		self.assertFalse(self.evolution.value == '173')