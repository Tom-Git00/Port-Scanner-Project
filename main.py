import socket
import time
import threading

def scanner_common(ip):

    """
    ip: alvo a analisar
    """
    # Lista de portas comuns a analisar
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5900, 8080]    
    start_time = time.time()    

    # Intera por cada porta na lista de common ports.
    for i in common_ports:
        # Cria um socket TCP, para enviar um IP
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, i))
            print(f"[+] Porta {i} está aberta")
            sock.close()
        except:
            None
        finally:
            sock.close()
    print("Analise completa. Demorou %s segundos para analisar a portas comuns." % (time.time() - start_time))


def scanner_ssh(ip):

    """
    ip: alvo a analisar
    """

    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, 22))
        print(f"[+] Porta 22 está aberta")
        sock.close()
    except:
        None
    finally:
        sock.close()
    print("Analise completa. Demorou %s segundos para analisar a porta ssh." % (time.time() - start_time))


def scanner_telnet(ip):

    """
    ip: alvo a analisar
    """
    start_time = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, 23))
        print(f"[+] Port 23 is open")
        sock.close()
    except:
        None

    print("Analise completa. Demorou %s segundos para analisar a porta telnet." % (time.time() - start_time))



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
            print(f"Thread {i+1}: Analisando portas {start_port}-{end_port}")

    for thread in threads:
        thread.join()
    
    print("-" * 50)
    print(f"Scan completed at: {time.ctime(time.time())}")
    print("Analise completa. Demorou %s para analisar todas as portas." % (time.time() - start_time))
    print(f"Total de portas encontradas: {len(open_ports)}")
    if open_ports:
        print(f"Portas abertas: {sorted(open_ports)}")
    else:
        print("Não foram encontradas portas abertas.")
    
    return sorted(open_ports)
            
def scan_port_range(ip, start_port, end_port, open_ports):

    for port in range(start_port, end_port + 1):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port}: Aberto")
        except socket.gaierror:
            # Invalido hostname
            print(f"Hostname invalido {ip}")
            pass
        except Exception as e:
            # Outro erro
            print(f"Erro {port}: {e}")
            pass
        finally:
            if sock:
                sock.close()

def main():
    maxthreads = 0
    portmax = 65000
    check_exit = False
    
    # Input do IP alvo
    ip_target = input("Enter target IP address: ")

    #Loop do menu
    while check_exit == False:
        print("1. Analisar portas comuns")
        print("2. Analisar todas as portas (0-65000)")
        print("3. Analisar porta ssh")
        print("4. Analisar porta telnet")
        print("5. Sair")

        #Variavel para escolher a opção do menu
        choice = input("Escolhe uma das opções: ")

        #If nested para escolher a opção do menu
        if(choice == '1'):
            print(f"Analisando portas communs {ip_target}...")
            scanner_common(ip_target)
        elif(choice == '2'):
            maxthreads = int(input("Intruduz o número de threads para a analise (default 100): ") or "100")
            print(f"Analisando todas as portas do alvo {ip_target}...")
            scanner_all_threading(ip_target, portmax, maxthreads)
        elif(choice == '3'):
            print(f"Analisando porta do ssh no alvo {ip_target}...")
            scanner_ssh(ip_target)
        elif(choice == '4'):
            print(f"Analisando porta do telnet no alvo {ip_target}...")
            scanner_telnet(ip_target)
        elif(choice == '5'):
            print("Saindo...")
            check_exit = True
        #Caso de invalidez
        else:
            print("Opção invalida. Por favor escolhe uma opção valida.")

if __name__ == "__main__":
    main()


