from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, send_file
from flask.helpers import flash
from .models import Money, Evolution
from . import db
from website.services.data_service import DataService
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import re
import io


views = Blueprint('views', __name__)

@views.route("/")
def index():
	my_moneys = DataService.my_money()
	global_amount = 0
	for money in my_moneys:
		global_amount = global_amount + float(money['quantity']) * (float(money['current_price']) - float(money['price']))

	if global_amount != 0:
		try:
			evol = Evolution(value=global_amount)
			db.session.add(evol)
			db.session.commit()
		except:
			pass

	return render_template('index.html', datas=my_moneys, global_amount=global_amount)


@views.route("/add", methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		name = request.form.get('money_name')
		value = request.form.get('money_value')
		quantity = request.form.get('money_quantity')
		regex = "^([0-9]+([.][0-9]*)?|[.][0-9]+)$"
		if not name or not value or not quantity or re.search(regex, value) == None or re.search(regex, quantity) == None:
			flash("Données incorrectes !", "alert")
		else:
			money = Money(name=name, value=value, quantity=quantity)
			db.session.add(money)
			db.session.commit()
			flash("Données enregistrées avec succès !", "success")

	return render_template('add.html', datas=DataService.datas_money())


@views.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
	money_to_delete = Money.query.get(id)
	if request.method == 'POST':
		db.session.delete(money_to_delete)
		db.session.commit()
		flash("Données supprimées avec succès !", "success")
		return redirect(url_for('views.index'))

	return render_template('delete.html', money=money_to_delete)

@views.route("/chart")
def chart():
	return render_template('chart.html')

@views.route("/visualize")
def visualize():
	evols = Evolution.query.all()
	N = len(evols)
	end = N
	if N > 10:
		start = N - 10
		N = end - start
	else:
		start = 0

	w_color = '#efefef'
	bg_color = '#100f0f'
	values = []
	dates = []
	for i in range(start, end):
		row = evols[i]
		values.append(float(row.value))
		dates.append(row.created.strftime("%d-%m\n%H:%M"))

	ind = np.arange(N) # the x locations for the groups
	
	fig, ax = plt.subplots()
	fig.set_facecolor(bg_color)

	def bar_color(val):
		return 'b' if val >= 0 else 'r'

	evols = ax.bar(ind, values, color=list(map(bar_color, values)))
	
	ax.set_facecolor(bg_color)
	ax.axhline(0, color='grey', linewidth=0.8)
	ax.set_xticks(ind)
	ax.set_xticklabels(labels=dates, fontdict={'multialignment': 'center'})
	ax.bar_label(evols, color=w_color, padding=3, labels=['%.0f €' % v for v in values])
	# fig.autofmt_xdate() # orientation of tick labels
	ax.tick_params(axis='x', colors=w_color)
	ax.tick_params(axis='y', colors=w_color)

	for direction in ["right", "top"]:
		ax.spines[direction].set_visible(False)
	
	for direction in ["left", "bottom"]:
		ax.spines[direction].set_color(w_color)

	canvas=FigureCanvas(fig)
	img = io.BytesIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='img/png')

@views.route("/trend/<periodicity>")
def trend(periodicity= '1h'):
	periodicity_filters = {'1h': '1<br>heure', '24h': '24<br>heures', '7d': '7<br>jours', '30d': '30<br>jours', '60d': '60<br>jours', '90d': '90<br>jours'}
	return render_template('trend.html', datas=DataService.datas_money(), filters=periodicity_filters, periodicity=periodicity)
