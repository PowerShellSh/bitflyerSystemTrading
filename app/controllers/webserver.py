from flask import Flask
from flask import render_template
from app.models.dfcandle import DataFrameCandle
import settings

app = Flask(__name__, template_folder='../views')

@app.route('/')
def index():

    df = DataFrameCandle(settings.product_code,
                         settings.trade_duration)
    df.set_all_candles(settings.past_period)
    candles = df.candles
    return render_template('./google.html', candles=candles)

def start():
    app.run(host='0.0.0.0', port=settings.web_port, threaded=True)
