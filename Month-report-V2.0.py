# Python 3.10.9
import xlsxwriter
import datetime
import string
import itertools
import subprocess as sp
import calendar
# Python 2.X
import commands
# Python 3.X
#import subprocess as sp
import os
"""
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
"""
ric_list = ["\.TW", "\.HK", "\.L", "\.SS", "\.SZ", "\.T", "\.NB", "\.OQ", "\.N", "\.A", "\.AX",
            "\.SI",
            "\.KL",
            "\.BK",
            "\.JK",
            "\.PS",
            "\.HSI",
            "\.DJI",
            "\.IXIC",
            "\.STI",
            "\.FTSE"]
# Replace with your list of variable names
client_list_user = ['sinopac01','iocbc01']
client_list = {'sinopac01': 'sino', 'iocbc01': 'iocbc'}


exchange_list = ['Taiwan Stock Exchage', 'Hong Kong Stock Exchange', 'UK - London Stock Exchange',
                 'China Shanghai Stock Exchange', 'China Shenzhen Stock Exchange', 'JP-Tokyo Stock Exchange',
                 'US-Nasdaq Basic',	'US - Nasdaq Floor RICs', 'US - NYSE Floor RICs', 'US - Amex Floor RICs',
                 'Australian Stock Exchange',	'Singapore',	'Malaysia',	'Thailand SET',	'Indonesia Stock Exchange(Jakarta)',
                 'Philippine Stock Exchange',	'HK-HSI',	'US-DJI',	'US-IXIC',	'SG-STI',	'UK-FTSE']


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
# last_month_of_year = '2022'
print("Last_Month_Of_Year", last_month_of_year)
# last_month = '12'
print("Last_Month", last_month)
# last_month_numberofdata = '31'
print("Last_Month_Number_Of_Data", last_month_numberofdata)

now = datetime.datetime.now()
numberofdata = calendar.monthrange(now.year, now.month)[1]

# Create a new workbook and add worksheets based on the length of the variable names list
workbook = xlsxwriter.Workbook(
    '/home/rjah/kwmok/wdss_prod_a/test_websocket streaming'+str(last_month)+'.xlsx')
wdss_logs_combine_sheet1 = workbook.add_worksheet("wdss-logs-combine")
wdss_logs_month_sheet2 = workbook.add_worksheet("wdss logs-"+str(last_month))

# Widen the first column to make the text clearer.
wdss_logs_combine_sheet1.set_column('A:A', 13)
wdss_logs_month_sheet2.set_column('A:A', 21)

clientsheets = {}  # Create an empty dictionary to store worksheet references
Unique_User = {}
for i in range(len(client_list_user)):
    worksheet = workbook.add_worksheet("Total connection "+client_list_user[i])
    # Store the worksheet reference in the dictionary
    clientsheets[client_list_user[i]] = worksheet
    clientsheets[client_list_user[i]].set_column('A:A', 12)
# Write data to the worksheets

Unique_User[len(client_list_user)+3] = workbook.add_worksheet("Unique User")
Unique_User[len(client_list_user)+3].set_column('A:A', 42)

# Add a bold format  and yellow color to use to highlight cells.
bold_yellow = workbook.add_format({'border': 2, 'bold': True})
bold_yellow.set_pattern(1)  # This is optional when using a solid fill.
bold_yellow.set_bg_color('yellow')

bold = workbook.add_format({'border': 2, 'bold': True})
border = workbook.add_format({'border': 2})

# The function is base on sheet


def wdss_logs_combine():
    print("Starting wdss_logs_combine sheet")
    # Text with formatting.
    # Add month of day  in row

    row_of_client = 1
    refer_data_row = 2

    for ref in client_list_user:
        for col_num, data in enumerate(range((int(last_month_numberofdata)+1))):
            wdss_logs_combine_sheet1.write(0, col_num, data, bold_yellow)
            wdss_logs_combine_sheet1.write(row_of_client, col_num, "='wdss logs-"+last_month+"'!" +
                                           excel_row[col_num]+str(refer_data_row)+"+'wdss logs-"+last_month+"'!"+excel_row[col_num]+str(refer_data_row+1), border)

        # Text with formatting.
        wdss_logs_combine_sheet1.write('A'+str(row_of_client+1), ref, bold)
        row_of_client += 1
        refer_data_row += 5

    # Write some simple text.
    wdss_logs_combine_sheet1.write('A1', 'User / Date', bold_yellow)
    print("wdss_logs_combine has been done")


def wdss_logs_month():
    print("Starting wdss_logs_month")
    row_1 = 1
    row_2 = 2
    zone_A = []
    zone_B = []
    # Python3
    # zone_A.clear()
    # zone_B.clear()
    del zone_A[:]
    del zone_B[:]
    for ref in client_list_user:
        # Python3
        # zone_A.clear()
        # zone_B.clear()
        del zone_A[:]
        del zone_B[:]
        # Add month of day  in row last_month_numberofdata
        for col_num, data in enumerate(range(1, int(last_month_numberofdata)+1)):
            # Python3
            # zone_A.clear()
            # zone_B.clear()
            del zone_A[:]
            del zone_B[:]
            # month number of data incolumn
            for i in range(len(client_list_user)):
                wdss_logs_month_sheet2.write(i*5, col_num+1, data, bold_yellow)
            
            # python 3.6
            #date = (f"{int(data):02}")
            
            # python 2.6
            date = "%02d" % data
            print(date)
            wdss_A = commands.getoutput("cat /home/rjah/kwmok/wdss_prod_a/wdss_logs/mon_non_closed_" +
                                        last_month_of_year+"-"+last_month+'-' + date+"_"+ref+".csv | awk -F ',' '{print $3}' | sort -u")
            wdss_B = commands.getoutput("cat /home/rjah/kwmok/wdss_prod_b/wdss_logs/mon_non_closed_" +
                                        last_month_of_year+"-"+last_month+'-' + date+"_"+ref+".csv | awk -F ',' '{print $3}' | sort -u")

            for A in wdss_A.split():
                zone_A.append(int(A))
            for B in wdss_B.split():
                zone_B.append(int(B))

            wdss_logs_month_sheet2.write(row_1, col_num+1, int(max(zone_A)), bold)
            wdss_logs_month_sheet2.write(row_2, col_num+1, int(max(zone_B)), bold)
            
        row_1 += 5
        row_2 += 5

    # row User / Date ,client A and B
    User_Date = 1
    client_Zone_A = 2
    client_Zone_B = 3
    for ref in client_list_user:
        wdss_logs_month_sheet2.write(
            'A'+str(User_Date), 'User / Date', bold_yellow)
        wdss_logs_month_sheet2.write(
            'A'+str(client_Zone_A), ref+'(Zone A)', bold)
        wdss_logs_month_sheet2.write(
            'A'+str(client_Zone_B), ref+'(Zone B)', bold)

        User_Date += 5
        client_Zone_A += 5
        client_Zone_B += 5
    print("wdss_logs_month has been done")


def Total_connection_sheet():
    print("Starting Total connection sheet")
    for i in range(len(client_list_user)):
        clientsheets[client_list_user[i]].write(
            'A1', client_list_user[i], bold_yellow)
        clientsheets[client_list_user[i]].write('A2', 'EX/ Month', bold_yellow)
        clientsheets[client_list_user[i]].write(
            'A3', (calendar.month_name[int(last_month)]), bold)
        clientsheets[client_list_user[i]].write(
            'W2', 'Total connection', bold_yellow)
        clientsheets[client_list_user[i]].write('W3', '=SUM(B3:V3)', border)
        for col_num, data in enumerate(exchange_list):
            clientsheets[client_list_user[i]].write(
                1, col_num+1, data, bold_yellow)
        
        for col_num, ric in enumerate(ric_list):
            wdss_A = commands.getoutput("grep -A1 -i auth  /home/rjah/kwmok/wdss_prod_a/wdss_logs/wds-servlet.log."+str(
                last_month_of_year)+"-"+str(last_month)+"-* |grep -A1 -i 'uid="+client_list[client_list_user[i]]+"' |grep Subscribe | grep '"+ric+",' |wc -l")
            wdss_B = commands.getoutput("grep -A1 -i auth  /home/rjah/kwmok/wdss_prod_b/wdss_logs/wds-servlet.log."+str(
                last_month_of_year)+"-"+str(last_month)+"-* |grep -A1 -i 'uid="+client_list[client_list_user[i]]+"' |grep Subscribe | grep '"+ric+",' |wc -l")
            clientsheets[client_list_user[i]].write(2, col_num+1, int(wdss_A)+int(wdss_B), border)
        
    print("Total_connection sheet has been done")


def Unique_User_sheeet():
    res = []
    ric_res = []
    market_unique_user = []
    total_unique_user = []
    market_unique_user_list = []
    row = 1
    A1 = 1
    A2 = 2
    A3 = 3
    x = 0
    for ref in client_list_user:
        for col_num, data in enumerate(exchange_list):
            Unique_User[len(client_list_user)+3].write(row,
                                                       col_num+1, data, bold_yellow)

        Unique_User[len(client_list_user)+3].write('A' +
                                                   str(A1), ref, bold_yellow)
        Unique_User[len(client_list_user)+3].write(
            'A'+str(A2), 'Unique User Count-Realtime exch data', bold_yellow)
        Unique_User[len(client_list_user)+3].write(
            'A'+str(A3), (calendar.month_name[int(last_month)]), bold)
        Unique_User[len(client_list_user)+3].write('W'+str(A2),
                                                   'Total unique user', bold_yellow)

        # Total unique user in W3
        
        total_unique_user_A = commands.getoutput(
            "grep -B1 'Subscribe' /home/rjah/kwmok/wdss_prod_a/wdss_logs/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}' |sort -u")
        total_unique_user_B = commands.getoutput(
            "grep -B1 'Subscribe' /home/rjah/kwmok/wdss_prod_b/wdss_logs/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}' |sort -u")

        for sub in total_unique_user_A.split()+total_unique_user_B.split():
            res.append(sub)

        for x in res:
            if x not in total_unique_user:
                total_unique_user.append(x)
        
        Unique_User[len(client_list_user)+3].write('W'+str(A3), len(total_unique_user), bold)
        
        # Python3
        # res.clear()
        # total_unique_user.clear()
        del res[:]
        del total_unique_user[:]
        # For unique_user by ric(exchange)
    
        for ric in ric_list:
            # Python3
            # market_unique_user.clear()
            # ric_res.clear()
            del market_unique_user[:]
            del ric_res[:]
            market_ric_A = commands.getoutput("grep -B1 'Subscribe' /home/rjah/kwmok/wdss_prod_a/wdss_logs/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                              ric+"'|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}'|sort -u")
            market_ric_B = commands.getoutput("grep -B1 'Subscribe' /home/rjah/kwmok/wdss_prod_b/wdss_logs/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                              ric+"'|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}'|sort -u")
            for sub in market_ric_A.split()+market_ric_B.split():
                ric_res.append(sub)
            for x in ric_res:
                if x not in market_unique_user:
                    market_unique_user.append(x)

            market_unique_user_list.append(len(market_unique_user))
            print(market_unique_user_list)
            
        for col_num, data in enumerate(market_unique_user_list):
            Unique_User[len(client_list_user)+3].write(A2,
                                                       col_num+1, data, bold)
        # Python3
        # market_unique_user_list.clear()
        del market_unique_user_list[:]
        row += 4
        A1 += 4
        A2 += 4
        A3 += 4
# insert Line Chart in wdss-logs-combine sheet.


def client_line_chart():
    chart = {}
    # Create a new chart object. In this case an embedded chart.
    for i in range(len(client_list_user)):
        chart[client_list_user[i]] = workbook.add_chart({'type': 'line'})

        # Configure the first series.
        chart[client_list_user[i]].add_series({
            'name':       "='wdss-logs-combine'!$A$"+str(i+2),
            'categories': "='wdss-logs-combine'!$B$1:$AF$1",
            'values':     "='wdss-logs-combine'!$B$"+str(i+2)+":$AF$"+str(i+2)
        })

        # Add a chart title and some axis labels.
        chart[client_list_user[i]].set_title({'name': client_list_user[i]+' max connection'})
        chart[client_list_user[i]].set_x_axis({'name': (calendar.month_name[int(last_month)])})
        chart[client_list_user[i]].set_y_axis({'name': 'Connection'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart[client_list_user[i]].set_style(10)
        # Insert the chart into the worksheet (with an offset).
        wdss_logs_combine_sheet1.insert_chart(
            'D'+str(i+5), chart[client_list_user[i]], {'x_offset': 25, 'y_offset': 10})



wdss_logs_combine()
wdss_logs_month()
Total_connection_sheet()
Unique_User_sheeet()
client_line_chart()
print("All sheets has been done.")

workbook.close()
