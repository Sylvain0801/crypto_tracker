from website.models import Money
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class DataService:

	def datas_money():
		url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
		parameters = {
			'start':'1',
			'limit':'50',
			'convert':'EUR'
		}
		headers = {
			'Accepts': 'application/json',
			'X-CMC_PRO_API_KEY': '50f847e2-b327-4ddf-9397-a55bd61cd2ec',
		}

		session = Session()
		session.headers.update(headers)
		try:
			response = session.get(url, params=parameters)
			datas = json.loads(response.text)
		except (ConnectionError, Timeout, TooManyRedirects) as e:
			print(e)
			
		return datas

	def my_money():
		datas = Money.query.all()
		my_moneys = []
		money_datas = DataService.datas_money()
		for data in datas:
			for money in money_datas['data']:
				if money['name'] == data.name:
					my_moneys.append({
						'id': money['id'],
						'money_id': data.id,
						'quantity': data.quantity,
						'symbol': money['symbol'],
						'name': money['name'],
						'trend': money['quote']['EUR']['percent_change_24h'],
						'price': data.value,
						'current_price': money['quote']['EUR']['price']
						})
					break
		
		return my_moneys

	