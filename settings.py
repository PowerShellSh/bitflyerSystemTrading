import configparser

from utils.utils import bool_from_str

conf = configparser.ConfigParser()
conf.read('settings.ini')

api_key = conf['bitflyer']['api_key']
api_account = conf['bitflyer']['api_account']
product_code = conf['bitflyer']['product_code']

db_name = conf['db']['name']
db_driver = conf['db']['driver']

web_port = int(conf['web']['port'])

trade_duration = conf['pytrading']['trade_duration'].lower()
back_test = bool_from_str(conf['pytrading']['back_test'])
use_percent = float(conf['pytrading']['use_percent'])
past_period = int(conf['pytrading']['past_period'])
stop_limit_percent = float(conf['pytrading']['stop_limit_percent'])
num_ranking = int(conf['pytrading']['num_ranking'])
