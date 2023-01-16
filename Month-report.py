#Python 3.10.9
import xlsxwriter
import datetime
import string
import itertools
import subprocess as sp
import calendar
import subprocess as sp
exchange_ric_list = {"Taiwan Stock Exchage": "\.TW",
                     'Hong Kong Stock Exchange': "\.HK",
                     'UK - London Stock Exchange': '\.L',
                     'China Shanghai Stock Exchange': '\.SS',
                     'China Shenzhen Stock Exchange': '\.SZ',
                     'JP-Tokyo Stock Exchange': '\.T',
                     'US-Nasdaq Basic': '\.NB',
                     'US - Nasdaq Floor RICs': '\.OQ',
                     'US - NYSE Floor RICs': '\.N',
                     'US - Amex Floor RICs': '\.A',
                     'Australian Stock Exchange': '\.AX',
                     'Singapore': '\.SI',
                     'Malaysia': '\.KL',
                     'Thailand SET': '\.BK',
                     'Indonesia Stock Exchange(Jakarta)': '\.JK',
                     'Philippine Stock Exchange': '\.PS',
                     'HK-HSI': '\.HSI',
                     'US-DJI': '\.DJI',
                     'US-IXIC': '\.IXIC',
                     'SG-STI': '\.STI',
                     'UK-FTSE': '\.FTSE'}

uid_client_list= ["sino","iocbc"]
client_list = {'sinopac01': 'sino', 'iocbc01': 'iocbc'}
zone_A = []
zone_B = []



# excel row A to AE
excel_row = list(
    itertools.chain(
        string.ascii_uppercase[0:30],
        (''.join(pair)
         for pair in itertools.product(string.ascii_uppercase[0:10], repeat=2))
    ))


# Getting today's date and the last month date
todayDate = datetime.date.today()
last_month_of_year = (todayDate.replace(
    day=1) - datetime.timedelta(days=1)).strftime("%Y")
last_month = (todayDate.replace(day=1) -
              datetime.timedelta(days=1)).strftime("%m")
last_month_numberofdata = (todayDate.replace(
    day=1) - datetime.timedelta(days=1)).strftime("%d")


for ref in range(len(client_list)):
    #print(col_num)
    print(ref+1)

for uid in client_list:
    print(uid)
#print(len(client_list))

