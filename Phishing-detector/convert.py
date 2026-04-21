import requests
import re
import csv
from urllib.parse import urlparse

def is_suspicious_url(url):
    """Check for obvious phishing patterns that should override model prediction"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.hostname or ""
        
        # Check if domain looks like an IP pattern (e.g., 123.123, 192.168.1.1)
        ip_pattern = re.match(r'^(\d{1,3}\.){1,3}\d{1,3}(:\d+)?$', domain)
        if ip_pattern:
            return True
        
        # Check if path contains a domain-like pattern (e.g., /google.com, /paypal.com)
        path = parsed.path or ""
        domain_in_path = re.search(r'/[a-zA-Z0-9-]+\.(com|net|org|edu|gov|co|io|me|tv|info|biz|us|uk|ca|au|de|fr|jp|cn|in|ru|br|mx|es|it|nl|se|no|dk|fi|pl|cz|gr|pt|ie|be|at|ch|tr|za|ae|sa|il|kr|tw|hk|sg|my|th|id|ph|vn|nz|jp|cn|in|ru|br|mx|es|it|nl|se|no|dk|fi|pl|cz|gr|pt|ie|be|at|ch|tr|za|ae|sa|il|kr|tw|hk|sg|my|th|id|ph|vn|nz)', path, re.IGNORECASE)
        if domain_in_path and domain and not any(legit in domain.lower() for legit in ['localhost', '127.0.0.1', '0.0.0.0']):
            return True
        
        # Check for suspicious patterns: IP-like domain with common service names in path
        suspicious_services = ['google', 'paypal', 'amazon', 'facebook', 'microsoft', 'apple', 'bank', 'login', 'signin', 'verify', 'secure', 'account']
        if ip_pattern or re.match(r'^(\d{1,3}\.)+\d{1,3}', domain):
            path_lower = path.lower()
            if any(service in path_lower for service in suspicious_services):
                return True
        
        return False
    except:
        return False

def convertion(url,prediction):
    name = []
    
    # Check for obvious phishing patterns first
    if is_suspicious_url(url):
        return [url,"Not Safe","Still want to Continue"]
    
    # found_url = find_url_in_csv('Datafiles/phishurls.csv', url)
    '''if "https://" in url:
        urlz = url.replace("https://","")
    if "http://" in url:
        urlz = url.replace("http://","")
    url_found = find_url_in_csv('Datafiles/legitimateurls.csv', urlz)'''
    
    if(shortlink(url)==-1):
        return [url,"Not Safe","Still want to Continue"]
    elif(prediction==1):
        return [url,"Safe","Continue","1"]
    else:
        return [url,"Not Safe","Still want to Continue"]
def shortlink(url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                          'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                          'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                          'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                          'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                          'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                          'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                          url)
        if match:
            return -1
        return 1
def find_url_in_csv(csv_file, target_url):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            url = row [0].strip() 
            if url == target_url:
                return url
    return None
