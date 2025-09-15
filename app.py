from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Secret key for session management

# Hardcoded stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2800,
    "AMZN": 3400,
    "MSFT": 300,
    "META": 320,    
    "NFLX": 410,    
    "NVDA": 460,    
    "INTC": 35,     
    "IBM": 135,     
    "ORCL": 125,    
    "ADBE": 500,    
    "PYPL": 75,     
    "CSCO": 55,     
    "CRM": 210,     
    "AMD": 120,     
    "QCOM": 145,    
    "SPOT": 160,    
    "UBER": 48,     
    "LYFT": 12,     
    "SHOP": 65,     
    "BA": 210,      
    "GE": 110,      
    "CAT": 270,     
    "GS": 340,      
    "JPM": 145,     
    "BAC": 29,      
    "WFC": 42,      
    "C": 45,        
    "V": 240,       
    "MA": 380,      
    "AXP": 165,     
    "PEP": 185,     
    "KO": 58,       
    "MCD": 290,     
    "SBUX": 100,    
    "NKE": 105
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'portfolio' not in session:
        session['portfolio'] = {}

    if request.method == 'POST':
        stock = request.form.get('stock')
        quantity = request.form.get('quantity')

        if stock in stock_prices and quantity.isdigit():
            quantity = int(quantity)
            if quantity > 0:
                if stock in session['portfolio']:
                    session['portfolio'][stock] += quantity
                else:
                    session['portfolio'][stock] = quantity
                session.modified = True

        return redirect(url_for('index'))

    portfolio = session['portfolio']
    detailed = []
    total_investment = 0

    for stock, qty in portfolio.items():
        price = stock_prices[stock]
        value = price * qty
        total_investment += value
        detailed.append({
            "stock": stock,
            "quantity": qty,
            "price": price,
            "value": value
        })

    result = {
        "detailed": detailed,
        "total": total_investment
    } if detailed else None

    return render_template('index.html', stocks=stock_prices.keys(), result=result)

@app.route('/reset')
def reset():
    session.pop('portfolio', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)