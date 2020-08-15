
import time
import hashlib
import requests
import urllib3
from lxml import etree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def xdl_proxy(orderno, secret, host, port):
    host_port = host + ":" + port
    # get sign
    timestamp = str(int(time.time()))              
    string = ""
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
    string = string.encode()
    md5_string = hashlib.md5(string).hexdigest()                
    sign = md5_string.upper()                             
    # get auth
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    proxy = { "http": "http://" + host_port, "https": "https://" + host_port}
    return proxy, auth