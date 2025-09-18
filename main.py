import socket
import sys
import time
import threading

def scanner_common(ip):
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5900, 8080]    
    start_time = time.time()    
    for i in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, i))
            print(f"[+] Port {i} is open")
            sock.close()
        except:
            None
        finally:
            sock.close()
    print("Scanning complete. It took %s seconds to scan cmon ports." % (time.time() - start_time))


def scanner_ssh(ip):
    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, 22))
        print(f"[+] Port 22 is open")
        sock.close()
    except:
        None
    finally:
        sock.close()
    print("Scanning complete. It took %s seconds to scan ssh port." % (time.time() - start_time))


def scanner_telnet(ip):
    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, 23))
        print(f"[+] Port 23 is open")
        sock.close()
    except:
        None
    finally:    
        sock.close()
    print("Scanning complete. It took %s seconds to scan telnet port." % (time.time() - start_time))


def scanner_all_threading(ip, portmax, maxthreads):

    """
    ip: alvo a analisar
    portmax: número máximo de portas a analisar {default: 65000}
    maxthreads: número máximo de threads a usar {default: 100}
    """

    print("starting scan on ip %s" % (ip))
    print("Scanning all {portmax} ports with {maxthreads} threads" % (portmax, maxthreads))
    print("Started at %s" % (time.ctime(time.time())))
    print("This may take a while...")
    start_time = time.time()

    ports_per_thread = portmax // maxthreads
    remainder = portmax % maxthreads
    threads = []
    open_ports = []

    for i in range(maxthreads):
        start_port = i * ports_per_thread + 1

        if i == maxthreads - 1:
            end_port = (i + 1) * ports_per_thread + remainder
        else: 
            end_port = (i + 1) + ports_per_thread

        #Verificar que não se ultrapassar o portmax
        end_port = min(end_port, portmax)

        if start_port <= portmax:
            None

def main():
    maxthreads = 0
    portmax = 65000
    check_exit = False
    
    ip_target = input("Enter target IP address: ")

    while check_exit == False:
        print("1. Scan common ports")
        print("2. Scan all ports (0-65000)")
        print("3. Scan SSH port")
        print("4. Scan Telnet port")
        print("3. Exit")

        choice = input("Choose on of the options): ")
        if(choice == '1'):
            print("Scanning common ports on target {ip_target}...")
            scanner_common(ip_target)
        elif(choice == '2'):
            None
        elif(choice == '3'):
            print("Scanning SSH port on target {ip_target}...")
            scanner_ssh(ip_target)
        elif(choice == '4'):
            print("Scanning Telnet port on target {ip_target}...")
            scanner_telnet(ip_target)
        elif(choice == '5'):
            print("Exiting...")
            check_exit = True

main()



