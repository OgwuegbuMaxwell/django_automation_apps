from django.shortcuts import get_object_or_404, redirect, render
from dal import autocomplete

from stockanalysis.utils import scrape_stock_data

from . models import Stock, StockData
from .forms import StockForm
from django.contrib import messages


def stocks(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST.get('stock')
            # fetch the stock and symbol
            stock = Stock.objects.get(pk=stock_id)
            symbol = stock.symbol
            exchange = stock.exchange
            stock_response = scrape_stock_data(symbol, exchange)
            
            # print(f"Stock ID: {stock_id}, Symbol: {symbol}, Exchange: {exchange}")
            # print(stock_response)
            
            if stock_response.get('current_price'):
                
                try:
                    stock_data = StockData.objects.get(stock=stock)
                except StockData.DoesNotExist:
                    stock_data = StockData(stock=stock)
                
                # Update the stock data instance with the response data
                
                # get all response data
                fifty_two_week_range = stock_response.get('fifty_two_week_range')
                if fifty_two_week_range:
                    week_52_low, week_52_high = fifty_two_week_range.split(' - ')
                else:
                    week_52_low, week_52_high = None, None
                # week_52_low, week_52_high = fifty_two_week_range.split(' - ')
                current_price = stock_response.get('current_price')
                previous_close = stock_response.get('previous_close')
                open_price = stock_response.get('open_price')
                price_changed = stock_response.get('price_change')
                percentage_changed = stock_response.get('percentage_changed')
                market_cap = stock_response.get('market_cap')
                pe_ratio = stock_response.get('pe_ratio')
                
                # Update stock data
                stock_data.current_price = current_price
                stock_data.price_changed = price_changed
                stock_data.percentage_changed = percentage_changed
                stock_data.previous_close = previous_close
                stock_data.week_52_high = week_52_high
                stock_data.week_52_low = week_52_low
                stock_data.market_cap = market_cap
                stock_data.pe_ratio = pe_ratio
                
                stock_data.save()
                # print('Data Updated')
                # messages.success(request, f"Form updated for: {symbol}")
                return redirect('stock_detail', stock_data.id)
                
                
            else:
                messages.error(request, f"Could not fetch the data for {symbol}")
                return redirect('stocks')

        else:
            messages.error(request, f"Invalid Form")
            return redirect('stocks')
    else:
        form = StockForm()
        context = {
            'form': form
        }
        return render(request, 'stockanalysis/stocks.html', context)


class StockAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Stock.objects.none()

        qs = Stock.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def stock_detail(request, pk):
    stock_data = get_object_or_404(StockData, pk=pk)
    context = {
        'stock_data':stock_data
    }
    
    return render(request, 'stockanalysis/stock-detail.html', context)



