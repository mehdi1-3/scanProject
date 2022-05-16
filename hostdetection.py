import nmap

def activeHosts(pool="192.168.14.0/24"): 
    scanner = nmap.PortScanner()
    scanner.scan(str(pool), arguments='-sn')
    for i in range(len(scanner.all_hosts())):
        print('host num {}: {}\n'.format(i, scanner.all_hosts()[i]))
        return scanner.all_hosts()