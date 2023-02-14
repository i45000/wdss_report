# Python 3.10.9
import xlsxwriter
import datetime
import string
import itertools
import subprocess as sp
import calendar
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

client_list = {'sinopac01': 'sino', 'iocbc01': 'iocbc'}
# , 'hsbc01': 'hsbc'}

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
print("Last_Month_Of_Year", last_month_of_year)
print("Last_Month", last_month)
print("Last_Month_Number_Of_Data", last_month_numberofdata)


now = datetime.datetime.now()
numberofdata = calendar.monthrange(now.year, now.month)[1]

# Create an new Excel file and add a worksheet1
workbook = xlsxwriter.Workbook(
    '/home/hli/Downloads/wds/B/websock streaming'+str(last_month)+'.xlsx')
worksheet1 = workbook.add_worksheet("wdss-logs-combine")
worksheet2 = workbook.add_worksheet("wdss logs-"+str(last_month))
worksheet3 = workbook.add_worksheet("Total connection sinopac01")
worksheet4 = workbook.add_worksheet("Total connection iocbc01")
worksheet5 = workbook.add_worksheet("Unique User sinopac01")
worksheet6 = workbook.add_worksheet("Unique User iocbc01")
worksheet7 = workbook.add_worksheet("Unique User")

"""
for ref in client_list.keys():
    print(ref)
    worksheet_name = "_workbook"
    client_ref=ref+worksheet_name
    client_ref= workbook.add_worksheet("Total connection  "+ref)

    for col_num, data in enumerate(exchange_list):
        client_ref.write(1, col_num+1, data)
"""



# Widen the first column to make the text clearer.
worksheet1.set_column('A:A', 13)
worksheet2.set_column('A:A', 21)
worksheet3.set_column('A:A', 12)
worksheet4.set_column('A:A', 12)
worksheet5.set_column('A:A', 42)
worksheet6.set_column('A:A', 42)


# Add a bold format  and yellow color to use to highlight cells.
bold_yellow = workbook.add_format({'border': 2, 'bold': True})
bold_yellow.set_pattern(1)  # This is optional when using a solid fill.
bold_yellow.set_bg_color('yellow')

bold = workbook.add_format({'border': 2, 'bold': True})
border = workbook.add_format({'border': 2})

# The function is base on sheet


def wdss_logs_combine():
    # Text with formatting.
    # Add month of day  in row

    row_of_client = 1
    refer_data_row = 2

    for ref in client_list.keys():
        for col_num, data in enumerate(range((numberofdata+1))):
            worksheet1.write(0, col_num, data, bold_yellow)
            worksheet1.write(row_of_client, col_num, "='wdss logs-"+last_month+"'!" +
                             excel_row[col_num]+str(refer_data_row)+"+'wdss logs-"+last_month+"'!"+excel_row[col_num]+str(refer_data_row+1), border)

        # Text with formatting.
        worksheet1.write('A'+str(row_of_client+1), ref, bold)
        row_of_client += 1
        refer_data_row += 5

    # Write some simple text.
    worksheet1.write('A1', 'User / Date', bold_yellow)


def wdss_logs_month():
    row_1 = 1
    row_2 = 2
    for ref in client_list.keys():
        zone_A = []
        zone_B = []
        zone_A.clear()
        zone_B.clear()
        # Add month of day  in row last_month_numberofdata
        for col_num, data in enumerate(range(1, int(last_month_numberofdata)+1)):
            zone_A.clear()
            zone_B.clear()

            worksheet2.write(0, col_num+1, data, bold_yellow)
            worksheet2.write(5, col_num+1, data, bold_yellow)
            date = (f"{int(data):02}")

            wdss_A = sp.getoutput("cat /home/hli/Downloads/wdss_prod_a/wdss_logs/mon_non/mon_non_closed_" +
                                  last_month_of_year+"-"+last_month+'-' + date+"_"+ref+".csv | awk -F ',' '{print $3}' | sort -u")
            wdss_B = sp.getoutput("cat /home/hli/Downloads/wdss_prod_b/wdss_logs/mon_non/mon_non_closed_" +
                                  last_month_of_year+"-"+last_month+'-' + date+"_"+ref+".csv | awk -F ',' '{print $3}' | sort -u")
            for A in wdss_A.split():
                zone_A.append(int(A))

            for B in wdss_B.split():
                zone_B.append(int(B))

            worksheet2.write(row_1, col_num+1, int(max(zone_A)), bold)
            worksheet2.write(row_2, col_num+1, int(max(zone_B)), bold)
        row_1 += 5
        row_2 += 5

    # row User / Date ,client A and B
    User_Date = 1
    client_Zone_A = 2
    client_Zone_B = 3
    for ref in client_list.keys():
        worksheet2.write('A'+str(User_Date), 'User / Date', bold_yellow)
        worksheet2.write('A'+str(client_Zone_A), ref+'(Zone A)', bold)
        worksheet2.write('A'+str(client_Zone_B), ref+'(Zone B)', bold)

        User_Date += 5
        client_Zone_A += 5
        client_Zone_B += 5


def Total_connection_sinopac01():
    for col_num, data in enumerate(exchange_list):
        worksheet3.write(1, col_num+1, data, bold_yellow)

    for col_num, ric in enumerate(exchange_ric_list.values()):
        wdss_A = sp.getoutput(
            "grep -A1 -i auth  /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-* |grep -A1 -i 'uid=sino' |grep Subscribe | grep '"+ric+",' |wc -l")
        wdss_B = sp.getoutput(
            "grep -A1 -i auth  /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-* |grep -A1 -i 'uid=sino' |grep Subscribe | grep '"+ric+",' |wc -l")
        worksheet3.write(2, col_num+1, int(wdss_A)+int(wdss_B), border)

    worksheet3.write('A1', 'sinopac01', bold_yellow)
    worksheet3.write('A2', 'EX/ Month', bold_yellow)
    worksheet3.write('A3', (calendar.month_name[int(last_month)]), bold)
    worksheet3.write('W2', 'Total connection', bold_yellow)
    worksheet3.write('W3', '=SUM(B3:V3)', border)


def Total_connection_iocbc01():
    for col_num, data in enumerate(exchange_list):
        worksheet4.write(1, col_num+1, data, bold_yellow)

    for col_num, ric in enumerate(exchange_ric_list.values()):
        wdss_A = sp.getoutput(
            "grep -A1 -i auth  /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-* |grep -A1 -i 'uid=iocbc' |grep Subscribe | grep '"+ric+",' |wc -l")
        wdss_B = sp.getoutput(
            "grep -A1 -i auth  /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-* |grep -A1 -i 'uid=iocbc' |grep Subscribe | grep '"+ric+",' |wc -l")
        worksheet4.write(2, col_num+1, int(wdss_A)+int(wdss_B), border)

    worksheet4.write('A1', 'iocbc01', bold_yellow)
    worksheet4.write('A2', 'EX/ Month', bold_yellow)
    worksheet4.write('A3', (calendar.month_name[int(last_month)]), bold)
    worksheet4.write('W2', 'Total connection', bold_yellow)
    worksheet4.write('W3', '=SUM(B3:V3)', border)


def Unique_User_sinopac01():
    res = []
    market_unique_user = []
    total_unique_user_sino = []

    market_unique_user_list = []
    for col_num, data in enumerate(exchange_list):
        worksheet5.write(1, col_num+1, data, bold_yellow)

    worksheet5.write('A1', 'sinopac01', bold_yellow)
    worksheet5.write('A2', 'Unique User Count-Realtime exch data', bold_yellow)
    worksheet5.write('A3', (calendar.month_name[int(last_month)]), bold)
    worksheet5.write('W2', 'Total unique user', bold_yellow)

    # For total unique user
    total_unique_user_sino_A = sp.getoutput(
        "grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid=sino' | awk -F '[ ,]' '{print $13}' |sort -u")
    total_unique_user_sino_B = sp.getoutput(
        "grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid=sino' | awk -F '[ ,]' '{print $13}' |sort -u")
    for sub in total_unique_user_sino_A.split()+total_unique_user_sino_B.split():
        res.append(sub)

    for x in res:
        if x not in total_unique_user_sino:
            total_unique_user_sino.append(x)

    # print(len(total_unique_user_sino))
    worksheet5.write('W3', len(total_unique_user_sino), bold)

    # For ric unique_user
    for ric in exchange_ric_list.values():
        market_unique_user.clear()
        res.clear()
        market_ric_A = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                    ric+"'|grep Authenticated | grep 'uid=sino' | awk -F '[ ,]' '{print $13}'|sort -u")
        market_ric_B = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                    ric+"'|grep Authenticated | grep 'uid=sino' | awk -F '[ ,]' '{print $13}'|sort -u")
        for sub in market_ric_A.split()+market_ric_B.split():
            res.append(sub)
        for x in res:
            if x not in market_unique_user:
                market_unique_user.append(x)

        market_unique_user_list.append(len(market_unique_user))
        print(market_unique_user_list)
    for col_num, data in enumerate(market_unique_user_list):
        worksheet5.write(2, col_num+1, data, bold)


def Unique_User_iocbc01():
    res = []
    market_unique_user = []
    total_unique_user_iocbc = []
    market_unique_user_list = []

    for col_num, data in enumerate(exchange_list):
        worksheet6.write(1, col_num+1, data, bold_yellow)

    worksheet6.write('A1', 'iocbc01', bold_yellow)
    worksheet6.write('A2', 'Unique User Count-Realtime exch data', bold_yellow)
    worksheet6.write('A3', (calendar.month_name[int(last_month)]), bold)
    worksheet6.write('W2', 'Total unique user', bold_yellow)

    total_unique_user_iocbc_A = sp.getoutput(
        "grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid=iocbc' | awk -F '[ ,]' '{print $13}' |sort -u")
    total_unique_user_iocbc_B = sp.getoutput(
        "grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid=iocbc' | awk -F '[ ,]' '{print $13}' |sort -u")

    for sub in total_unique_user_iocbc_A.split()+total_unique_user_iocbc_B.split():
        res.append(sub)

    for x in res:
        if x not in total_unique_user_iocbc:
            total_unique_user_iocbc.append(x)

    # print(len(total_unique_user_iocbc))
    worksheet6.write('W3', len(total_unique_user_iocbc), bold)

    # For unique_user by ric(exchange)
    for ric in exchange_ric_list.values():
        market_unique_user.clear()
        res.clear()
        market_ric_A = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                    ric+"'|grep Authenticated | grep 'uid=iocbc' | awk -F '[ ,]' '{print $13}'|sort -u")
        market_ric_B = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                    ric+"'|grep Authenticated | grep 'uid=iocbc' | awk -F '[ ,]' '{print $13}'|sort -u")
        for sub in market_ric_A.split()+market_ric_B.split():
            res.append(sub)
        for x in res:
            if x not in market_unique_user:
                market_unique_user.append(x)

        market_unique_user_list.append(len(market_unique_user))
        print(market_unique_user_list)
    for col_num, data in enumerate(market_unique_user_list):
        worksheet6.write(2, col_num+1, data, bold)


def Unique_User():
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
    for ref in client_list.keys():
        for col_num, data in enumerate(exchange_list):
            worksheet7.write(row, col_num+1, data, bold_yellow)

        worksheet7.write('A'+str(A1), ref, bold_yellow)
        worksheet7.write(
            'A'+str(A2), 'Unique User Count-Realtime exch data', bold_yellow)
        worksheet7.write(
            'A'+str(A3), (calendar.month_name[int(last_month)]), bold)
        worksheet7.write('W'+str(A2), 'Total unique user', bold_yellow)

        # Total unique user in W3
        total_unique_user_A = sp.getoutput(
            "grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}' |sort -u")
        total_unique_user_B = sp.getoutput(
            "grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}' |sort -u")

        for sub in total_unique_user_A.split()+total_unique_user_B.split():
            res.append(sub)

        for x in res:
            if x not in total_unique_user:
                total_unique_user.append(x)

        worksheet7.write('W'+str(A3), len(total_unique_user), bold)

        res.clear()
        total_unique_user.clear()

        # For unique_user by ric(exchange)
        for ric in exchange_ric_list.values():
            market_unique_user.clear()
            ric_res.clear()
            market_ric_A = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/A/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                        ric+"'|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}'|sort -u")
            market_ric_B = sp.getoutput("grep -B1 'Subscribe' /home/hli/Downloads/wds/B/wds-servlet.log."+last_month_of_year+"-"+last_month+"-*| grep -B1 '" +
                                        ric+"'|grep Authenticated | grep 'uid="+client_list[ref]+"' | awk -F '[ ,]' '{print $13}'|sort -u")
            for sub in market_ric_A.split()+market_ric_B.split():
                ric_res.append(sub)
            for x in ric_res:
                if x not in market_unique_user:
                    market_unique_user.append(x)

            market_unique_user_list.append(len(market_unique_user))
            print(market_unique_user_list)
        for col_num, data in enumerate(market_unique_user_list):
            worksheet7.write(A2, col_num+1, data, bold)
        market_unique_user_list.clear()
        row += 4
        A1 += 4
        A2 += 4
        A3 += 4
#insert Line Chart in wdss-logs-combine sheet.
def client_line_chart():
    
    # Create a new chart object. In this case an embedded chart.
    chart1 = workbook.add_chart({'type': 'line'})
    chart2 = workbook.add_chart({'type': 'line'})

    # Configure the first series.
    chart1.add_series({
        'name':       "='wdss-logs-combine'!$A$2",
        'categories': "='wdss-logs-combine'!$B$1:$AF$1",
        'values':     "='wdss-logs-combine'!$B$2:$AF$2"
    })

    chart2.add_series({
        'name':       "='wdss-logs-combine'!$A$3",
        'categories': "='wdss-logs-combine'!$B$1:$AF$1",
        'values':     "='wdss-logs-combine'!$B$3:$AF$3"
    })

    # Add a chart title and some axis labels.
    chart1.set_title ({'name': 'sinopac max connection'})
    chart1.set_x_axis({'name': (calendar.month_name[int(last_month)])})
    chart1.set_y_axis({'name': 'Connection'})

    chart2.set_title ({'name': 'iocbc max connection'})
    chart2.set_x_axis({'name': (calendar.month_name[int(last_month)])})
    chart2.set_y_axis({'name': 'Connection'})

    # Set an Excel chart style. Colors with white outline and shadow.
    chart1.set_style(10)
    chart2.set_style(10)
    # Insert the chart into the worksheet (with an offset).
    worksheet1.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    worksheet1.insert_chart('D7', chart2, {'x_offset': 25, 'y_offset': 10})


wdss_logs_combine()
wdss_logs_month()
Total_connection_sinopac01()
Total_connection_iocbc01()
Unique_User_sinopac01()
Unique_User_iocbc01()
Unique_User()
client_line_chart()
print("All sheets has been done.")

workbook.close()
