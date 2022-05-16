import sys
import nmap  
import json



try:
    nm = nmap.PortScanner()  # instantiate nmap.PortScanner object
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)



def osdetection(adresse):
    scanner = nm.scan(adresse, arguments='-O')
    length = len(scanner['scan'][adresse]['osmatch'])
    if length == 0:
        return json.dumps("unknown")
    else:
        result = {}
        name = scanner['scan'][adresse]['osmatch'][0]['name']
        accuracy = scanner['scan'][adresse]['osmatch'][0]['accuracy']
        vendor = scanner['scan'][adresse]['osmatch'][0]['osclass'][0]['vendor']
        osfamily = scanner['scan'][adresse]['osmatch'][0]['osclass'][0]['osfamily']
        result['adresse'] = adresse
        result['name'] = name
        result['accuracy'] = accuracy
        result['vendor'] = vendor
        result['osfamily'] = osfamily
        return json.dumps(result)


