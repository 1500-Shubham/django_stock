from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


def home(request):
	#pk_c44fa98bc83a49afbe259d49ef16dfe9
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_c44fa98bc83a49afbe259d49ef16dfe9")

		try:
			api=json.loads(api_request.content)
		except Exception as e:
			api="Error"
		return render(request, 'home.html', {'api':api})

	else:
		return render(request, 'home.html', {'ticker':"Enter Company Symbol Above"})




def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json

	if request.method== 'POST': #for database insert form needed advance way
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request,("Stock has been added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		#name hai sirf ticker naam ka now api call karke saare name ka data extract kar lo boom and pass it to page
		output =[]
		for ticker_items in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_items) +"/quote?token=pk_c44fa98bc83a49afbe259d49ef16dfe9")

			try:
				api=json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api="Error"


		return render(request, 'add_stock.html', {'ticker':ticker, 'output':output} )

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request,("Stock has been deleted!"))
	return redirect(delete_stock)

def delete_stock(request):
	import requests
	import json

	ticker = Stock.objects.all()

	return render(request, 'delete_stock.html', {'ticker':ticker} )


	


