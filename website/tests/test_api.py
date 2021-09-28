import unittest
from website.services.data_service import DataService

class ApiTests(unittest.TestCase):
	def setUp(self):
		self.moneys = DataService.datas_money()
	
	def test_count_result(self):
		self.assertEqual(len(self.moneys['data']), 50)

	def test_type_result(self):
		self.assertEqual(type(self.moneys), dict)
	
	def test_EUR_results(self):
		for money in self.moneys['data']:
			self.assertTrue('EUR' in money['quote'])