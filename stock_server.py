from flask import Flask, render_template
import pandas as pd

import quandl
quandl.ApiConfig.api_key = "zC992yeEkw5VTye5PFJY"

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route('/')
@app.route('/stocks/')
def stocks():
    # provide a list of shocks
    stocks = [
        'AAPL', 'MSFT', 'GOOG', 'AMZN',
        'EBAY', 'CSCO', 'TSLA', 'QCOM',
        'PETX', 'CLNE', 'AXAS', 'IPAR'
        ]
    return render_template('index.html', stocks=stocks)


@app.route('/stocks/<ticker>/')
def chart(ticker):
    # query data from the Quandl
    data = quandl.get_table(
        'WIKI/PRICES',
        qopts={'columns': ['ticker', 'date', 'close']},
        ticker=[ticker],
        date={'gte': '2016-01-01'}
        )
    
    # convert timestamp into string time of format 'YYYY-MM-DD'
    data['date'] = pd.to_datetime(data['date'], unit='d')
    dates = data['date'].dt.strftime('%Y-%m-%d').tolist()
    prices = data['close'].tolist()
    
    # calculate the moving average
    N = len(prices)
    movingAverages = [0 for _ in range(N)]
    movingAverages[0] = prices[0]
    movingAverages[-1] = prices[-1]
    mean_moving = 0
    for i in range(1, N-1):
        if i < 50:
            movingAverages[i] = sum(prices[:2*i])/(2*i)
            mean_moving = movingAverages[i]
        elif i >= N-50:
            movingAverages[i] = sum(prices[i-(N-i):])/(2*(N-i))
        else:
            mean_moving = mean_moving-prices[i-50]/100+prices[i+50]/100
            movingAverages[i] = mean_moving
    
    return render_template('chart.html', dates=dates, prices=prices, movingAverages=movingAverages)

if __name__ == '__main__':
    app.secret_key = 'super-secret-key'
    app.debug = True
    app.run(host='localhost', port=7777)
