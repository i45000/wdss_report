import pysftp
import fnmatch
import datetime
import time
import schedule
import os
import paramiko

from dateutil.relativedelta import relativedelta

host_dev_140 = '172.30.10.140'
host_dev_141 = '172.30.10.141'
port_dev = 22
username_dev = 'root'
password_dev = 'P@ssw0rd'
privateKeyFilePath = "disable"

Dev_140_wdss_log_a = '/home/rjah/kwmok/wdss_prod_a/wdss_logs/'
Dev_140_wdss_log_b = '/home/rjah/kwmok/wdss_prod_b/wdss_logs/'
Dev_140_wdss_log_OutPut_a = '/home/rjah/kwmok/wdss_prod_a/output/'
Dev_140_wdss_log_OutPut_b = '/home/rjah/kwmok/wdss_prod_b/output/'


Dev_141_wdss_log_a = '/home/rjah/kwmok/wdss_11_prod_a/wdss_logs/'
Dev_141_wdss_log_b = '/home/rjah/kwmok/wdss_11_prod_b/wdss_logs/'

wdss_checkLog_a = "/home/rjah/kwmok/wdss_prod_a/checkLog3.sh"
wdss_checkLog_b = "/home/rjah/kwmok/wdss_prod_b/checkLog3.sh"

wdss_checkLog_11_a = "/home/rjah/kwmok/wdss_11_prod_a/checkLog3.sh"
wdss_checkLog_11_b = "/home/rjah/kwmok/wdss_11_prod_b/checkLog3.sh"

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

# wdss-11-A-Pro
wdss_11_A_Pro_ip_address = '10.10.51.13'
wdss_11_A_Pro_port = 27522
# wdss_username_A_pro = 'root'
# wdss_password_A_pro = 'p@ssw0rd'

# wdss-11-B-Pro
wdss_11_B_Pro_ip_address = '10.10.52.13'
wdss_11_B_Pro_port = 27522
# wdss_username_A_pro = 'root'
# wdss_password_B_pro = 'p@ssw0rd'


# From upload windows to 172.30.10.140
# Local window path
Mywin_Dir_A = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\A\\'
Mywin_Dir_B = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\B\\'

MyWin_Dir_wdss_11_A = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\wdss-11-A\\'
MyWin_Dir_wdss_11_B = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\wdss-11-B\\'

# MyWin_Dir_wdss_12_A = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\wdss-11-A\\'
# MyWin_Dir_wdss_12_B = 'C:\\Users\\hli\\OneDrive - Vocational Training Council\\Labci\\wds\\wdss-11-B\\'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# -------------------------------------------------------------------
three_months_ago = (datetime.datetime.today() -
                    relativedelta(months=3)).strftime("%Y-%m")

client_list = {'sinopac01': 'sino', 'iocbc01': 'iocbc'}
client_list_wdss_11 = {'sbinbtv01': 'sbi'}

file_time = (datetime.datetime.today() -
             datetime.timedelta(days=2)).strftime("%Y-%m-%d")
print(file_time)
max_attempts = 3
f = open('C:\\Users\\hli\\Desktop\\Python\\output_log_FTP.txt', 'a')

def time_stamp():
    execute_date = (datetime.datetime.today() -
                    datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    return execute_date


def clear_log_statistics_stamp():
    three_months_ago = (datetime.datetime.today() -
                        relativedelta(months=3)).strftime("%Y-%m")
    return three_months_ago


def do_ssh_command_140():
    # Open the file for writing
    print("running nohup command")
    f.write('running nohup command')
    delete_keyword = ["ERROR", "Error", "Instrument",
                      "Unwatch", "Accepted", "Auto-close", "Closing...", "Unsubscribe", "Watch:"]
    # 04-05-2023  #05-05-2023   #06-05-2023
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_dev_140, port_dev, username_dev, password_dev)
        wds_log_name_date = "wds-servlet.log."+time_stamp()
        for word in delete_keyword:
            # delete the delete_keyword in log
            clearn_error_command_A = "sed -i '/"+word + \
                "/d' " + Dev_140_wdss_log_a + wds_log_name_date
            clearn_error_command_B = "sed -i '/"+word + \
                "/d' " + Dev_140_wdss_log_b + wds_log_name_date

            (stdin, stdout, stderr) = ssh.exec_command(clearn_error_command_A)
            (stdin, stdout, stderr) = ssh.exec_command(clearn_error_command_B)
            # cmd_output = stdout.read()
            # print('log printing A: ', command_A, cmd_output)
            time.sleep(3)
        """
        if output is None:
            print("successful to clear the error log")
        else:
            print("fail to clear the error log")
        """
        for client_name in client_list.keys():
            command_A = 'nohup ' + wdss_checkLog_a+' -d ' + \
                time_stamp()+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &'
            (stdin, stdout, stderr) = ssh.exec_command(command_A)
            # cmd_output = stdout.read()
            # print('log printing A: ', command_A, cmd_output)
            print(client_name + " : "+command_A)
            f.write(client_name + " : "+command_A)
            command_B = 'nohup ' + wdss_checkLog_b+' -d ' + \
                time_stamp()+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &'
            (stdin, stdout, stderr) = ssh.exec_command(command_B)
            # print(stdout)
            # cmd_output = stdout.read()
            # print('log printing B: ', command_B, cmd_output)
            print(client_name + " : "+command_B)
            f.write(client_name + " : "+command_B)

        (stdin, stdout, stderr) = ssh.exec_command("disown -a")
        print("Done")

    finally:
        ssh.close()
        print("Close SSH")


def download_wdss_log_A_pro():
    print("Stating in wdss A production")
    wdss_log_filename_A1 = ("wds-servlet.log."+time_stamp())

    for attempt in range(max_attempts):
        try:
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
                break
        except paramiko.ssh_exception.SSHException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    else:
        print(f"Failed to connect after {max_attempts} attempts")



def download_wdss_log_B_pro():
    print("Starting in wdss B production")
    wdss_log_filename_B1 = ("wds-servlet.log." + time_stamp())
    for attempt in range(max_attempts):
        try:
            with pysftp.Connection(
                host=host_B_pro,
                port=port_B_pro,
                username=username_B_pro,
                password=password_B_pro,
                cnopts=cnopts,
            ) as serv_details:
                print("Successfully in Zone B")
                for filename in serv_details.listdir("/efs-log/rjah/"):
                    if fnmatch.fnmatch(filename, wdss_log_filename_B1):
                        print("Downloading in B .......")
                        serv_details.get(
                            "/efs-log/rjah/" + filename,
                            preserve_mtime=True,
                            localpath=Mywin_Dir_B + filename,
                        )
                        print(filename, "downloaded successfully in Zone B")
                serv_details.close()
                print("End and close in wdss B")
                break
        except paramiko.ssh_exception.SSHException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    else:
        print(f"Failed to connect after {max_attempts} attempts")


def upload_wdss_log_to_140():
    print("Stating in wdss A")
    f.write("Stating in wdss A")
    wdss_log_filename_A_B_fullname = ("wds-servlet.log."+time_stamp())
    print("wdss_log_file_download", wdss_log_filename_A_B_fullname)
    f.write("wdss_log_file_download", wdss_log_filename_A_B_fullname)
    with pysftp.Connection(host=host_dev_140, port=port_dev, username=username_dev, password=password_dev, cnopts=cnopts) as serv_details:
        print("successfully in Zone A")
        f.write("successfully in Zone A")
        for relPath, dirs, files in os.walk(Mywin_Dir_A):
            if (wdss_log_filename_A_B_fullname in files):
                fullPath = os.path.join(
                    Mywin_Dir_A, relPath, wdss_log_filename_A_B_fullname)
                print(fullPath)
                f.write(fullPath)
                print("Upload in A .......")
                f.write("Upload in A .......")        
                serv_details.put(fullPath, Dev_140_wdss_log_a +
                                 wdss_log_filename_A_B_fullname)
                print(wdss_log_filename_A_B_fullname,
                      "uploaded successfully in Zone A")
                f.write(wdss_log_filename_A_B_fullname,
                      "uploaded successfully in Zone A")        
        for relPath, dirs, files in os.walk(Mywin_Dir_B):
            if (wdss_log_filename_A_B_fullname in files):
                fullPath = os.path.join(
                    Mywin_Dir_B, relPath, wdss_log_filename_A_B_fullname)
                print(fullPath)
                f.write(fullPath)
                print("Upload in B .......")
                f.write("Upload in B .......")
                serv_details.put(fullPath, Dev_140_wdss_log_b +
                                 wdss_log_filename_A_B_fullname)
                print(wdss_log_filename_A_B_fullname,
                      "uploaded successfully in Zone B")
                f.write(wdss_log_filename_A_B_fullname,
                      "uploaded successfully in Zone B")

        serv_details.close()
    print("End upload and close in wdss A and B")
    f.write("End upload and close in wdss A and B")

# ----------------------------------------------------------------------------------
def download_wdss_log_11_pro():
    print("Stating in wdss_11_A production")
    wdss_log_filename_11 = ("wds-servlet.log."+time_stamp())
    with pysftp.Connection(host=wdss_11_A_Pro_ip_address, port=wdss_11_A_Pro_port, username=username_A_pro, password=password_A_pro, cnopts=cnopts) as serv_details:
        print("successfully in Zone A")
        for filename in serv_details.listdir('/efs-log/rjah/'):
            if fnmatch.fnmatch(filename, wdss_log_filename_11):
                print("Downloading in wdss_11_A .......")
                serv_details.get(
                    '/efs-log/rjah/'+filename, preserve_mtime=True, localpath=MyWin_Dir_wdss_11_A+filename)
                print(filename, "downloaded successfully in Zone A")

    serv_details.close()
    print("End and close in wdss_11_A")

    print("Stating in wdss_11_B production")
    with pysftp.Connection(host=wdss_11_B_Pro_ip_address, port=wdss_11_B_Pro_port, username=username_A_pro, password=password_A_pro, cnopts=cnopts) as serv_details:
        print("successfully in Zone B")
        for filename in serv_details.listdir('/efs-log/rjah/'):
            if fnmatch.fnmatch(filename, wdss_log_filename_11):
                print("Downloading in wdss_11_B .......")
                serv_details.get(
                    '/efs-log/rjah/'+filename, preserve_mtime=True, localpath=MyWin_Dir_wdss_11_B+filename)
                print(filename, "downloaded successfully in Zone B")

    serv_details.close()
    print("End and close in wdss_11_B")


def upload_wdss_log_11_to_141():

    print("Stating in wdss_11_A")
    wdss_log_filename_11 = ("wds-servlet.log."+time_stamp())
    print("wdss_log_file_download", wdss_log_filename_11)
    with pysftp.Connection(host=host_dev_141, port=port_dev, username=username_dev, password=password_dev, cnopts=cnopts) as serv_details:
        print("successfully in Zone A")
        for relPath, dirs, files in os.walk(MyWin_Dir_wdss_11_A):
            if (wdss_log_filename_11 in files):
                fullPath = os.path.join(
                    MyWin_Dir_wdss_11_A, relPath, wdss_log_filename_11)
                print(fullPath)
                print("Upload in A .......")
                serv_details.put(fullPath, Dev_141_wdss_log_a +
                                 wdss_log_filename_11)
                print(wdss_log_filename_11,
                      "uploaded successfully in Zone A")

    serv_details.close()

    time.sleep(5)

    print("Stating in wdss_11_B")
    wdss_log_filename_11 = ("wds-servlet.log."+time_stamp())
    print("wdss_log_file_download", wdss_log_filename_11)
    with pysftp.Connection(host=host_dev_141, port=port_dev, username=username_dev, password=password_dev, cnopts=cnopts) as serv_details:
        print("successfully in Zone B")
        for relPath, dirs, files in os.walk(MyWin_Dir_wdss_11_B):
            if (wdss_log_filename_11 in files):
                fullPath = os.path.join(
                    MyWin_Dir_wdss_11_B, relPath, wdss_log_filename_11)
                print(fullPath)
                print("Upload in B .......")
                serv_details.put(fullPath, Dev_141_wdss_log_b +
                                 wdss_log_filename_11)
                print(wdss_log_filename_11,
                      "uploaded successfully in Zone B")

    serv_details.close()


def do_ssh_execute_command_for_wdss_11_pro_in_141():
    print('running nohup command')
    delete_keyword = ["ERROR", "Error", "Instrument",
                      "Unwatch", "Accepted", "Auto-close", "Unsubscribe"]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_dev_141, port_dev, username_dev, password_dev)
        wds_log_name_date = "wds-servlet.log."+time_stamp()
        for word in delete_keyword:
            # delete the error in log
            clearn_error_command_A = "sed -i '/"+word + \
                "/d' " + Dev_141_wdss_log_a + wds_log_name_date
            clearn_error_command_B = "sed -i '/"+word + \
                "/d' " + Dev_141_wdss_log_b + wds_log_name_date

            (stdin, stdout, stderr) = ssh.exec_command(clearn_error_command_A)
            (stdin, stdout, stderr) = ssh.exec_command(clearn_error_command_B)
            # cmd_output = stdout.read()
            # print('log printing A: ', command_A, cmd_output)
            time.sleep(3)
        """
        if output is None:
            print("successful to clear the error log")
        else:
            print("fail to clear the error log")
        """
        for client_name in client_list_wdss_11.keys():
            command_A = 'nohup ' + wdss_checkLog_11_a+' -d ' + \
                time_stamp()+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &'
            (stdin, stdout, stderr) = ssh.exec_command(command_A)
            # cmd_output = stdout.read()
            # print('log printing A: ', command_A, cmd_output)
            print(client_name + " : "+command_A)

            command_B = 'nohup ' + wdss_checkLog_11_b+' -d ' + \
                time_stamp()+' -s "00:00:00" -e "23:59:59" -u'+client_name+' -t0 &'
            (stdin, stdout, stderr) = ssh.exec_command(command_B)
            # print(stdout)
            # cmd_output = stdout.read()
            # print('log printing B: ', command_B, cmd_output)
            print(client_name + " : "+command_B)

        (stdin, stdout, stderr) = ssh.exec_command("disown -a")
        print("Complete command")

    finally:
        ssh.close()
        print("Close SSH")

# ----------------------------------------------------------------------------------
def clear_old_log_statistics_for_wds():

    clearn_wdss_logs_command_A = "rm -f " + \
        Dev_140_wdss_log_a+"*"+clear_log_statistics_stamp()+"*"
    clearn_wdss_logs_command_B = "rm -f " + \
        Dev_140_wdss_log_b+"*"+clear_log_statistics_stamp()+"*"

    clearn_OutPut_command_A = "rm -f " + \
        Dev_140_wdss_log_OutPut_a+"*"+clear_log_statistics_stamp()+"*"
    clearn_OutPut_command_B = "rm -f " + \
        Dev_140_wdss_log_OutPut_b+"*"+clear_log_statistics_stamp()+"*"
    clear_nohub_out = "rm -f " + \
        Dev_140_wdss_log_a+"nohup.out"
    #print(clear_nohub_out)
    print(clearn_wdss_logs_command_A)
    print(clearn_wdss_logs_command_B)

    print(clearn_OutPut_command_A)
    print(clearn_OutPut_command_B)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_dev_140, port_dev, username_dev, password_dev)

        (stdin, stdout, stderr) = ssh.exec_command(clearn_wdss_logs_command_A)
        (stdin, stdout, stderr) = ssh.exec_command(clearn_wdss_logs_command_B)
        (stdin, stdout, stderr) = ssh.exec_command(clearn_OutPut_command_A)
        (stdin, stdout, stderr) = ssh.exec_command(clearn_OutPut_command_B)
    finally:
        ssh.close()
        print("Close SSH")


schedule.every().day.at("10:15").do(download_wdss_log_A_pro)
schedule.every().day.at("10:18").do(download_wdss_log_B_pro)

schedule.every().day.at("10:20").do(upload_wdss_log_to_140)

schedule.every().day.at("10:22").do(do_ssh_command_140)
# ---------------------------------------------------------------------
# schedule.every().day.at("16:30").do(download_wdss_log_11_pro)
# schedule.every().day.at("16:32").do(upload_wdss_log_11_to_141)
# schedule.every().day.at("16:34").do(do_ssh_execute_command_for_wdss_11_pro_in_141)

#schedule.every().month.at("08:00").do(clear_old_log_statistics_for_wds)
schedule.every().sunday.at("09:00").do(clear_old_log_statistics_for_wds)


while True:
    schedule.run_pending()
    time.sleep(3)
