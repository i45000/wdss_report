import pysftp
import fnmatch
import datetime
import time
import schedule
import os
import paramiko

host_dev = '172.30.10.140'
port_dev = 22
username_dev = 'root'
password_dev = 'P@ssw0rd'
privateKeyFilePath = "disable"

Dev_wdss_log_a = '/home/rjah/kwmok/wdss_prod_a/wdss_logs/'
Dev_wdss_log_b = '/home/rjah/kwmok/wdss_prod_b/wdss_logs/'
wdss_checkLog_a = "/home/rjah/kwmok/wdss_prod_a/checkLog3.sh"
wdss_checkLog_b = "/home/rjah/kwmok/wdss_prod_b/checkLog3.sh"

# wdss-A-Pro
host_A_pro = '10.10.51.14'
port_A_pro = 27522
username_A_pro = 'root'
password_A_pro = 'p@ssw0rd'

# wdss-B-Pro
host_B_pro = '10.10.52.14'
port_B_pro = 27522
username_B_pro = 'root'
password_B_pro = 'p@ssw0rd'

# From upload windows to 172.30.10.140
# Local window path
Mywin_Dir_A = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\A\\'
Mywin_Dir_B = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\B\\'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Getting today's date and the last month date
todayDate = datetime.date.today()
last_month_of_year = (todayDate.replace(
    day=1) - datetime.timedelta(days=1)).strftime("%Y")
last_month = (todayDate.replace(day=1) -
              datetime.timedelta(days=1)).strftime("%m")
last_month_numberofdata = (todayDate.replace(
    day=1) - datetime.timedelta(days=1)).strftime("%d")
Previous_Date = datetime.datetime.today() - datetime.timedelta(days=30)  # n=1
# print("Last_Month_Of_Year", last_month_of_year)
# print("Last_Month", last_month)
# print("Last_Month_Number_Of_Data", last_month_numberofdata)
# print("Previous_Date.day",Previous_Date.strftime("%Y-%m-%d"))

client_list = {'sinopac01': 'sino', 'iocbc01': 'iocbc'}

file_time = ("wds-servlet.log."+(datetime.datetime.today() -
             datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
print(file_time)


# output_file = 'paramiko.org'

def do_ssh_command():
    print('running nohup command')
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_dev, port_dev, username_dev, password_dev)

        for client_name in client_list.keys():
            command_A = 'nohup ' +wdss_checkLog_a+' -d '+(datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &' 
            (stdin, stdout, stderr) = ssh.exec_command(command_A)
            #cmd_output = stdout.read()
            #print('log printing A: ', command_A, cmd_output)
            print(client_name + " command_A")
            
            command_B = 'nohup ' + wdss_checkLog_b+' -d '+(datetime.datetime.today() - datetime.timedelta(
                days=3)).strftime("%Y-%m-%d")+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &'
            print(command_B)
            (stdin, stdout, stderr) = ssh.exec_command(command_B)
            print(stdout)
            #cmd_output = stdout.read()
            #print('log printing B: ', command_B, cmd_output)
            print(client_name + " command_B")
            
        (stdin, stdout, stderr) = ssh.exec_command("disown -a")
        print("Done")

    finally:
        ssh.close()
        print("Close SSH")


def download_wdss_log_A_pro():
    print("Stating in wdss A production")
    wdss_log_filename_A1 = ("wds-servlet.log."+(datetime.datetime.today() -
                            datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
    with pysftp.Connection(host=host_A_pro, port=port_A_pro, username=username_A_pro, password=password_A_pro, cnopts=cnopts) as serv_details:
        print("successfully in Zone A")
        for filename in serv_details.listdir('/efs-log/rjah/'):
            if fnmatch.fnmatch(filename, wdss_log_filename_A1):
                print("Downloading in A .......")
                serv_details.get(
                    '/efs-log/rjah/'+filename, preserve_mtime=True, localpath=Mywin_Dir_A+filename)
                print(filename, "downloaded successfully in Zone A")

    serv_details.close()
    print("End and close in wdss A")


def download_wdss_log_B_pro():
    print("Stating in wdss B production")
    wdss_log_filename_B1 = ("wds-servlet.log."+(datetime.datetime.today() -
                            datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
    with pysftp.Connection(host=host_B_pro, port=port_B_pro, username=username_B_pro, password=password_B_pro, cnopts=cnopts) as serv_details:
        print("successfully in Zone B")
        for filename in serv_details.listdir('/efs-log/rjah/'):
            if fnmatch.fnmatch(filename, wdss_log_filename_B1):
                print("Downloading in B .......")
                serv_details.get(
                    '/efs-log/rjah/'+filename, preserve_mtime=True, localpath=Mywin_Dir_B+filename)
                print(filename, "downloaded successfully in Zone B")

    serv_details.close()
    print("End and close in wdss B")


def upload_wdss_log_A():
    print("Stating in wdss A")
    wdss_log_filename_test_A1 = (
        "wds-servlet.log."+(datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
    wdss_log_filename_test_2 = (
        "wds-servlet.log."+(datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %S"))
    print("wdss_log_file_download", wdss_log_filename_test_2)
    with pysftp.Connection(host=host_dev, port=port_dev, username=username_dev, password=password_dev, cnopts=cnopts) as serv_details:
        print("successfully in Zone A")
        for relPath, dirs, files in os.walk(Mywin_Dir_A):
            if (wdss_log_filename_test_A1 in files):
                fullPath = os.path.join(
                    Mywin_Dir_A, relPath, wdss_log_filename_test_A1)
                print(fullPath)
                print("Upload in A .......")
                serv_details.put(fullPath, Dev_wdss_log_a +
                                 wdss_log_filename_test_A1)
                print(wdss_log_filename_test_A1,
                      "uploaded successfully in Zone AXXXXXXXXXX")
        # time.sleep(3)

    serv_details.close()
    print("End and close in wdss A")


def upload_wdss_log_B():
    print("Stating in wdss B")
    wdss_log_filename_test_B1 = (
        "wds-servlet.log."+(datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d"))
    wdss_log_filename_test_2 = (
        "wds-servlet.log."+(datetime.datetime.today() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %S"))
    print("wdss_log_file_download", wdss_log_filename_test_2)
    with pysftp.Connection(host=host_dev, port=port_dev, username=username_dev, password=password_dev, cnopts=cnopts) as serv_details:
        print("successfully in Zone B")
        for relPath, dirs, files in os.walk(Mywin_Dir_B):
            if (wdss_log_filename_test_B1 in files):
                fullPath = os.path.join(
                    Mywin_Dir_B, relPath, wdss_log_filename_test_B1)
                print(fullPath)
                print("Upload in B .......")
                serv_details.put(fullPath, Dev_wdss_log_b +
                                 wdss_log_filename_test_B1)
                print(wdss_log_filename_test_B1,
                      "uploaded successfully in Zone BXXXXXXXXXX")
 
    serv_details.close()
    print("End and close in wdss B")



schedule.every().day.at("01:00").do(download_wdss_log_A_pro)
schedule.every().day.at("01:02").do(download_wdss_log_B_pro)

schedule.every().day.at("01:04").do(upload_wdss_log_A)
schedule.every().day.at("01:06").do(upload_wdss_log_B)

schedule.every().day.at("01:08").do(do_ssh_command)


while True:
    schedule.run_pending()
    time.sleep(2)
