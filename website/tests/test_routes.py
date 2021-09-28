import unittest
import sqlite3
from website import create_app


class RouteTests(unittest.TestCase):
	def setUp(self):
		app = create_app()
		app.config['TESTING'] = True
		self.app = app.test_client()

	def test_main_page(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_add_page(self):
		response = self.app.get('/add', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_chart_page(self):
		response = self.app.get('/chart', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_trend_page(self):
		periodicity_filters = {
			'1h': '1<br>heure', 
			'24h': '24<br>heures', 
			'7d': '7<br>jours', 
			'30d': '30<br>jours', 
			'60d': '60<br>jours', 
			'90d': '90<br>jours'
		}
		for key in periodicity_filters:
			response = self.app.get(f'/trend/{key}', follow_redirects=True)
			self.assertEqual(response.status_code, 200)

	def test_delete_page(self):
		con = sqlite3.connect('website/crypto.db')
		c = con.cursor()
		c.execute("SELECT * FROM money")
		datas = c.fetchall()
		if datas:
			for data in datas:
				response = self.app.get(f'/delete/{data[0]}', follow_redirects=True)
				self.assertEqual(response.status_code, 200)
		else:
			print('Table money is empty')
		
if __name__ == "__main__":
	unittest.main()