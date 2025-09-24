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

    print("Scanning complete. It took %s seconds to scan telnet port." % (time.time() - start_time))



def scanner_all_threading(ip, portmax, maxthreads):

    """
    ip: alvo a analisar
    portmax: número máximo de portas a analisar {default: 65000}
    maxthreads: número máximo de threads a usar {default: 100}
    """

    print("starting scan on ip %s" % (ip))
    print("Scanning all %d ports with %d threads" % (portmax, maxthreads))
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
            end_port = (i + 1) * ports_per_thread

        #Verificar que não se ultrapassar o portmax
        end_port = min(end_port, portmax)

        if start_port <= portmax:
            thread = threading.Thread(target=scan_port_range, args=(ip, start_port, end_port, open_ports))
            threads.append(thread)
            thread.start()
            print(f"Thread {i+1}: Scanning ports {start_port}-{end_port}")

    for thread in threads:
        thread.join()
    
    print("-" * 50)
    print(f"Scan completed at: {time.ctime(time.time())}")
    print("Scanning complete. It took %s seconds to scan all ports." % (time.time() - start_time))
    print(f"Total open ports found: {len(open_ports)}")
    if open_ports:
        print(f"Open ports: {sorted(open_ports)}")
    else:
        print("No open ports found")
    
    return sorted(open_ports)
            
def scan_port_range(ip, start_port, end_port, open_ports):
    """Scan a range of ports for a given IP"""
    for port in range(start_port, end_port + 1):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port}: Open")
        except socket.gaierror:
            # Couldn't resolve hostname
            pass
        except Exception as e:
            # Other socket errors
            pass
        finally:
            if sock:
                sock.close()



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
        print("5. Exit")

        choice = input("Choose one of the options: ")
        if(choice == '1'):
            print(f"Scanning common ports on target {ip_target}...")
            scanner_common(ip_target)
        elif(choice == '2'):
            maxthreads = int(input("Enter max number of threads (default 100): ") or "100")
            print(f"Scanning all ports on target {ip_target}...")
            scanner_all_threading(ip_target, portmax, maxthreads)
        elif(choice == '3'):
            print(f"Scanning SSH port on target {ip_target}...")
            scanner_ssh(ip_target)
        elif(choice == '4'):
            print(f"Scanning Telnet port on target {ip_target}...")
            scanner_telnet(ip_target)
        elif(choice == '5'):
            print("Exiting...")
            check_exit = True

if __name__ == "__main__":
    main()


