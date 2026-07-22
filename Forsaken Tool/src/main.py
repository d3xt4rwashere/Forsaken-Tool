import os
import sys
import subprocess
import argparse
import socket
import hashlib
import ssl
import urllib.parse
from datetime import datetime

def auto_install(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
    except ImportError:
        print(f"[*] '{package_name}' not found. Installing silently in the background, please wait...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            print(f"[+] '{package_name}' installed successfully!")
        except Exception as e:
            print(f"[-] Failed to install '{package_name}': {e}\nPlease install it manually using 'pip install {package_name}'.")
            sys.exit(1)

auto_install("requests")
auto_install("phonenumbers")
auto_install("Pillow", "PIL")
auto_install("dnspython", "dns")
auto_install("PyPDF2")
auto_install("python-docx", "docx")

import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from PIL import Image, ExifTags
import dns.resolver
import PyPDF2
from docx import Document

__version__ = "1.2.1"
__author__ = "By D3xt4r"

if os.name == 'nt':
    os.system('')

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
W = "\033[0m"
C = "\033[36m"
O = "\033[38;5;208m"

REPORT_FILE = "forsaken_report.txt"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def log_to_report(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_content = content.replace(R, "").replace(G, "").replace(Y, "").replace(W, "").replace(C, "").replace(O, "")
    try:
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {clean_content}\n")
    except Exception:
        pass

def print_header():
    banner = f"""{R}
    ███████╗ ██████╗ ██████╗  ██████╗ █████╗ ██╗  ██╗███████╗███╗   ██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝████╗  ██║
    █████╗  ██║   ██║██████╔╝███████║███████║█████╔╝ █████╗  ██╔██╗ ██║
    ██╔══╝  ██║   ██║██╔══██╗╚════██║██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║
    ██║     ╚██████╔╝██║  ██║███████║██║  ██║██║  ██╗███████║██║ ╚████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
                                                                       
           ████████╗ ██████╗  ██████╗ ██╗                              
           ╚══██╔══╝██╔═══██╗██╔═══██╗██║                              
              ██║   ██║   ██║██║   ██║██║                              
              ██║   ██║   ██║██║   ██║██║                              
              ██║   ╚██████╔╝╚██████╔╝████████╗                     
              ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝                     
    {W}"""
    print(banner)
    border = f"{R}{'='*78}{W}"
    print(border)
    print(f"[*] FORSAKEN TOOL v{__version__} | Auto-Deploy UI | {__author__}")
    print(f"{C}[+] Session log active -> {REPORT_FILE}{W}")
    print(border + "\n")

def geolocate_ip(ip_address):
    msg = f"[*] Querying IP Geolocation: {ip_address}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=10)
        data = response.json()
        if data.get('status') == 'success':
            res = (f"[+] RESULTS:\n"
                   f"    - Country/City: {data.get('country')} / {data.get('city')}\n"
                   f"    - Region/ZIP:   {data.get('regionName')} / {data.get('zip')}\n"
                   f"    - ISP:          {data.get('isp')}\n"
                   f"    - AS Number:    {data.get('as')}\n"
                   f"    - Coordinates:  {data.get('lat')}, {data.get('lon')}")
            print(f"{G}{res}{W}"); log_to_report(res)
        else:
            err = "[-] ERROR: IP not found or invalid."
            print(f"{R}{err}{W}"); log_to_report(err)
    except Exception as e:
        print(f"{R}[-] Connection Error: {e}{W}")

def phone_recon(phone_number):
    msg = f"[*] Analyzing Phone Number: {phone_number}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        parsed_num = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_valid_number(parsed_num):
            country = geocoder.description_for_number(parsed_num, "en")
            operator = carrier.name_for_number(parsed_num, "en")
            res = (f"[+] RESULTS:\n"
                   f"    - Validity: Valid Number\n"
                   f"    - Country:  {country}\n"
                   f"    - Carrier:  {operator if operator else 'Unknown'}\n"
                   f"    - Format (E164): {phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164)}")
            print(f"{G}{res}{W}"); log_to_report(res)
        else:
            err = "[-] ERROR: Invalid phone number format."
            print(f"{R}{err}{W}"); log_to_report(err)
    except Exception as e:
        print(f"{R}[-] Analysis Error: {e}{W}")

def username_recon(username):
    msg = f"[*] Scanning Username Across Global Networks: {username}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    targets = {
        "GitHub": f"https://github.com/{username}",
        "Linktree": f"https://linktr.ee/{username}",
        "Roblox": f"https://www.roblox.com/user.aspx?username={username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Chess.com": f"https://www.chess.com/member/{username}",
        "Replit": f"https://replit.com/@{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Behance": f"https://www.behance.net/{username}",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "DockerHub": f"https://hub.docker.com/u/{username}",
        "Keybase": f"https://keybase.io/{username}",
        "Last.fm": f"https://www.last.fm/user/{username}",
        "Scribd": f"https://www.scribd.com/{username}",
        "SlideShare": f"https://www.slideshare.net/{username}",
        "Tumblr": f"https://{username}.tumblr.com",
        "Wattpad": f"https://www.wattpad.com/user/{username}",
        "Wikipedia": f"https://en.wikipedia.org/wiki/User:{username}",
        "Letterboxd": f"https://letterboxd.com/{username}/",
        "Patreon": f"https://www.patreon.com/{username}",
        "ProductHunt": f"https://www.producthunt.com/@{username}",
        "DailyMotion": f"https://www.dailymotion.com/{username}",
        "Bandcamp": f"https://bandcamp.com/{username}",
        "Imgur": f"https://imgur.com/user/{username}",
        "BuyMeACoffee": f"https://www.buymeacoffee.com/{username}",
        "Hackernews": f"https://news.ycombinator.com/user?id={username}"
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    found_any = False
    for platform, url in targets.items():
        try:
            res = requests.get(url, headers=headers, timeout=4)
            if res.status_code == 200:
                hit = f"[+] FOUND [{platform}]: {url}"
                print(f"{G}{hit}{W}"); log_to_report(hit)
                found_any = True
        except requests.RequestException:
            continue
    if not found_any:
        print(f"{R}[-] No active profiles found in core database.{W}")

def get_decimal_from_dms(dms, ref):
    try:
        degrees = float(dms[0])
        minutes = float(dms[1]) / 60.0
        seconds = float(dms[2]) / 3600.0
        val = degrees + minutes + seconds
        if ref in ['S', 'W']:
            val = -val
        return round(val, 6)
    except Exception:
        return 0.0

def exif_location_extractor(image_path):
    msg = f"[*] Extracting EXIF Data from: {image_path}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if not exif_data:
            print(f"{R}[-] No EXIF metadata found in image.{W}")
            return

        geotagging = {}
        for (idx, tag) in ExifTags.TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif_data:
                    print(f"{R}[-] No GPS coordinates found in EXIF.{W}")
                    return
                for (key, val) in ExifTags.GPSTAGS.items():
                    if key in exif_data[idx]:
                        geotagging[val] = exif_data[idx][key]
        
        if 'GPSLatitude' not in geotagging or 'GPSLongitude' not in geotagging:
            print(f"{R}[-] No GPS coordinates found in EXIF.{W}")
            return

        lat = get_decimal_from_dms(geotagging['GPSLatitude'], geotagging.get('GPSLatitudeRef', 'N'))
        lon = get_decimal_from_dms(geotagging['GPSLongitude'], geotagging.get('GPSLongitudeRef', 'E'))

        maps_url = f"https://www.google.com/maps?q={lat},{lon}"
        res = (f"[+] GPS DATA FOUND!\n"
               f"    - Latitude:  {lat}\n"
               f"    - Longitude: {lon}\n"
               f"    - Target Link: {maps_url}")
        print(f"{G}{res}{W}"); log_to_report(res)

    except FileNotFoundError:
        print(f"{R}[-] ERROR: Image file not found. Check the path.{W}")
    except Exception as e:
        print(f"{R}[-] EXIF Extraction Error: {e}{W}")

def subdomain_scanner(domain):
    msg = f"[*] Mapping Subdomains for: {domain}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    common_subs = ["www", "mail", "ftp", "admin", "api", "blog", "dev", "cpanel"]
    for sub in common_subs:
        target_url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target_url)
            hit = f"[+] ACTIVE SUBDOMAIN: {target_url} -> IP: {ip}"
            print(f"{G}{hit}{W}"); log_to_report(hit)
        except socket.gaierror:
            continue

def dns_lookup(domain):
    msg = f"[*] Querying DNS Zones for: {domain}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        res = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}", timeout=10)
        if res.status_code == 200 and "error" not in res.text.lower():
            print(f"{G}[+] DNS RECORDS OUT:{W}\n{res.text}")
            log_to_report(res.text)
        else:
            print(f"{R}[-] Could not resolve zone data.{W}")
    except Exception as e:
        print(f"{R}[-] DNS Fetch Error: {e}{W}")

def http_header_grab(domain):
    msg = f"[*] Grabbing HTTP Headers from: {domain}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    url = domain if domain.startswith(("http://", "https://")) else f"https://{domain}"
    try:
        res = requests.get(url, timeout=5, allow_redirects=True)
        print(f"{G}[+] HEADERS GRABBED:{W}")
        interesting_headers = ["Server", "Content-Type", "X-Frame-Options", "Content-Security-Policy"]
        for header in interesting_headers:
            val = res.headers.get(header, "Not Set (Risk)")
            color = G if "Not Set" not in val else R
            print(f"    - {header}: {color}{val}{W}")
    except Exception as e:
        print(f"{R}[-] Failed to establish HTTP handshake: {e}{W}")

def quick_port_scan(target):
    msg = f"[*] Launching Stealth Port Scan on: {target}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 8080: "Proxy"}
    try:
        target_ip = socket.gethostbyname(target)
        for port, service in common_ports.items():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(f"{G}[+] PORT OPEN: {port} ({service}){W}")
            s.close()
    except Exception as e:
        print(f"{R}[-] Scan aborted: {e}{W}")

def whois_lookup(domain):
    msg = f"[*] Fetching WHOIS Ownership Records: {domain}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        res = requests.get(f"https://api.hackertarget.com/whois/?q={domain}", timeout=10)
        if res.status_code == 200 and "error" not in res.text.lower():
            print(f"{G}[+] RESULTS:{W}\n{res.text}")
        else:
            print(f"{R}[-] WHOIS data unavailable.{W}")
    except Exception as e:
        print(f"{R}[-] WHOIS Error: {e}{W}")

def reverse_dns(ip_address):
    msg = f"[*] Checking Reverse DNS for IP: {ip_address}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        host, aliases, ip_list = socket.gethostbyaddr(ip_address)
        print(f"{G}[+] Hostname Found: {host}{W}")
    except socket.herror:
        print(f"{R}[-] No PTR records found.{W}")

def mac_lookup(mac_address):
    msg = f"[*] Mapping Hardware Vendor for MAC: {mac_address}"
    print(f"{Y}{msg}{W}"); log_to_report(msg)
    try:
        res = requests.get(f"https://api.macvendors.com/{mac_address}", timeout=10)
        if res.status_code == 200:
            print(f"{G}[+] Hardware Manufacturer: {res.text}{W}")
        else:
            print(f"{R}[-] Database lookup failed.{W}")
    except Exception as e:
        print(f"{R}[-] Lookup Error: {e}{W}")

def data_breach_lookup(email):
    msg = f"[*] Checking Data Breaches for: {email}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    try:
        res = requests.get(f"https://api.xposedornot.com/v1/check-email/{email}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            breaches = data.get("breaches", [[]])[0]
            if breaches:
                res_msg = f"[!] CAUTION: {len(breaches)} platform(s) breached!"
                print(f"{R}{res_msg}{W}"); log_to_report(res_msg)
                for b in breaches:
                    print(f"    {R}-> {b}{W}")
            else:
                print(f"{G}[+] No breaches found. Looks clean!{W}")
        elif res.status_code == 404:
            print(f"{G}[+] No breaches found. Looks clean!{W}")
        else:
            print(f"{R}[-] API Server Error or Rate Limit hit.{W}")
    except Exception as e:
        print(f"{R}[-] Data Breach Check Error: {e}{W}")

def metadata_cleaner(image_path):
    msg = f"[*] Anti-OSINT: Scrubbing EXIF metadata from: {image_path}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    try:
        img = Image.open(image_path)
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)
        
        if '.' in image_path:
            clean_path = f"{image_path.rsplit('.', 1)[0]}_anon.{image_path.rsplit('.', 1)[1]}"
        else:
            clean_path = f"{image_path}_anon.png"
            
        image_without_exif.save(clean_path)
        res = f"[+] SUCCESS: Image completely anonymized!\n    -> Saved to: {clean_path}"
        print(f"{G}{res}{W}"); log_to_report(res)
    except FileNotFoundError:
        print(f"{R}[-] ERROR: Image not found.{W}")
    except Exception as e:
        print(f"{R}[-] Failed to clean image metadata: {e}{W}")

def email_osint(email):
    msg = f"[*] Running Deep Email OSINT on: {email}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    domain = email.split('@')[-1] if '@' in email else ""
    
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f"{G}[+] MX Records Found (Domain accepts mail):{W}")
        for rdata in mx_records:
            print(f"    - {rdata.exchange} (Pref: {rdata.preference})")
    except Exception:
        print(f"{R}[-] No MX records. Email might be invalid or spoofed/temp mail.{W}")
    
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    try:
        res = requests.get(f"https://en.gravatar.com/{email_hash}.json", headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code == 200:
            data = res.json().get('entry', [])[0]
            profile_url = data.get('profileUrl')
            username = data.get('preferredUsername')
            print(f"{G}[+] Gravatar Profile Found!{W}")
            print(f"    - Username: {username}")
            print(f"    - Profile Link: {profile_url}")
            log_to_report(f"Gravatar Hit: {username} | {profile_url}")
        else:
            print(f"{Y}[-] No public Gravatar profile linked to this email.{W}")
    except Exception as e:
        print(f"{R}[-] Gravatar check error: {e}{W}")

def leak_osint_search(query_term):
    msg = f"[*] Querying Leak OSINT Intelligence Network for: {query_term}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    try:
        url = f"https://api.xposedornot.com/v1/breach-analytics?email={query_term}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if "Error" not in data:
                print(f"{G}[+] LEAK INTEL FOUND:{W}")
                print(f"    - Exposed Records: {data.get('ExposedRecords', 'Unknown')}")
                print(f"    - Breaches Count: {data.get('BreachesCount', 'Unknown')}")
                print(f"    - Past Passwords Found: {'Yes' if data.get('PasswordsExposed') else 'No'}")
            else:
                print(f"{R}[-] No direct intelligence match found for this query.{W}")
        else:
            print(f"{R}[-] Leak intelligence node unreachable.{W}")
    except Exception as e:
        print(f"{R}[-] Leak OSINT Error: {e}{W}")

def hash_analyzer(hash_str):
    msg = f"[*] Analyzing Hash Algorithm & Intel: {hash_str}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    length = len(hash_str.strip())
    print(f"{G}[+] Hash Length: {length} characters{W}")
    
    algo = "Unknown"
    if length == 32: algo = "MD5 / NTLM"
    elif length == 40: algo = "SHA-1"
    elif length == 64: algo = "SHA-256"
    elif length == 128: algo = "SHA-512"
    
    print(f"{G}[+] Estimated Algorithm: {algo}{W}")
    try:
        res = requests.get(f"https://api.ha.information-security.it/v1/?hash={hash_str}", timeout=5)
        if res.status_code == 200:
            print(f"[+] Online Database Result:\n{res.text}")
        else:
            print(f"{Y}[-] Not found in quick online public lookup tables.{W}")
    except Exception:
        print(f"{Y}[-] Online hash DB lookup skipped/unreachable.{W}")

def wifi_recon(mac_or_ssid):
    msg = f"[*] Running Wi-Fi / MAC Recon for: {mac_or_ssid}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    if ":" in mac_or_ssid or "-" in mac_or_ssid:
        try:
            res = requests.get(f"https://api.macvendors.com/{mac_or_ssid}", timeout=8)
            if res.status_code == 200:
                print(f"{G}[+] Wireless Adapter / Router Vendor: {res.text}{W}")
                print(f"    - Security Profile: Standard IEEE 802.11 AP/Client")
            else:
                print(f"{R}[-] Vendor lookup failed.{W}")
        except Exception as e:
            print(f"{R}[-] Error: {e}{W}")
    else:
        print(f"{G}[+] SSID Target Analysis: {mac_or_ssid}{W}")
        print(f"    - Estimated Default WPS Pin Generator algorithm: Check router label model.")
        print(f"    - Common default security check: WPA2-PSK / WPA3 transition mode recommended.")

def web_vulnerability_scanner(domain):
    msg = f"[*] Running Web Quick Vulnerability / Fuzzing Scan: {domain}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    base_url = domain if domain.startswith(("http://", "https://")) else f"https://{domain}"
    endpoints = ["/robots.txt", "/sitemap.xml", "/.git/HEAD", "/admin/", "/backup.zip", "/config.json", "/api/"]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    for ep in endpoints:
        target = base_url.rstrip('/') + ep
        try:
            r = requests.get(target, headers=headers, timeout=4, allow_redirects=False)
            if r.status_code == 200:
                print(f"{R}[!] EXPOSED / OPEN [200]: {target}{W}")
                log_to_report(f"Exposed: {target}")
            elif r.status_code in [403, 401]:
                print(f"{Y}[+] Protected [{r.status_code}]: {target}{W}")
            else:
                print(f"    - Checked: {ep} (Status: {r.status_code})")
        except Exception:
            continue

def doc_metadata_cleaner(file_path):
    msg = f"[*] Anti-OSINT Document Shield: Cleaning Metadata from {file_path}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    print(f"{C}[+] Feature Highlights: Defense-oriented, ideal for journalists & researchers.{W}")
    try:
        if file_path.lower().endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_path)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            clean_path = file_path.rsplit('.', 1)[0] + "_anon.pdf"
            with open(clean_path, 'wb') as f:
                writer.write(f)
            print(f"{G}[+] SUCCESS: PDF metadata wiped! Saved to: {clean_path}{W}")
            
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            core_props = doc.core_properties
            core_props.author = "Anonymous"
            core_props.last_modified_by = "Anonymous"
            core_props.comments = ""
            core_props.category = ""
            
            clean_path = file_path.rsplit('.', 1)[0] + "_anon.docx"
            doc.save(clean_path)
            print(f"{G}[+] SUCCESS: DOCX metadata wiped! Saved to: {clean_path}{W}")
        else:
            print(f"{R}[-] Unsupported format. Provide a .pdf or .docx file.{W}")
    except Exception as e:
        print(f"{R}[-] Document cleaning error: {e}{W}")

def url_analyzer(target_url):
    msg = f"[*] Analyzing URL Structure, Redirects & SSL: {target_url}"
    print(f"{O}{msg}{W}"); log_to_report(msg)
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url
        
    try:
        parsed = urllib.parse.urlparse(target_url)
        print(f"{G}[+] URL Components:{W}")
        print(f"    - Scheme: {parsed.scheme}")
        print(f"    - Domain: {parsed.netloc}")
        print(f"    - Path:   {parsed.path if parsed.path else '/'}")
        print(f"    - Query:  {parsed.query if parsed.query else 'None'}")
        
        res = requests.get(target_url, timeout=6, allow_redirects=True)
        print(f"\n{G}[+] Redirect Chain & Status:{W}")
        print(f"    - Final Status Code: {res.status_code}")
        print(f"    - Total Redirects: {len(res.history)}")
        for resp in res.history:
            print(f"      -> Redirected from {resp.url} (Status: {resp.status_code})")
        print(f"      -> Final Destination: {res.url}")
        
        if parsed.scheme == 'https':
            print(f"\n{G}[+] SSL / TLS Certificate Analysis:{W}")
            ctx = ssl.create_default_context()
            with socket.create_connection((parsed.netloc, 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname=parsed.netloc) as ssock:
                    cert = ssock.getpeercert()
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    print(f"    - Issued To (CN): {subject.get('commonName', 'Unknown')}")
                    print(f"    - Issued By (Org): {issuer.get('organizationName', 'Unknown')}")
                    print(f"    - Valid Until: {cert.get('notAfter', 'Unknown')}")
    except Exception as e:
        print(f"{R}[-] URL Analysis Error: {e}{W}")

def osint_searchers_menu():
    while True:
        clear_screen()
        print_header()
        print(f"{C}==== [ SUB-MENU: OSINT SEARCHERS ] ===={W}\n")
        print(f"{R}[01]{W} IP Geolocation Lookup         {R}[02]{W} Phone Number Recon")
        print(f"{R}[03]{W} Username Scanner              {R}[04]{W} EXIF Image Geo-Locator")
        print(f"{R}[05]{W} <-- Back to Main Menu")
        
        choice = input(f"\n{Y}[?] Select a searcher: {W}").strip()
        if choice in ["1", "01"]:
            ip = input("[*] Enter Target IP: ").strip()
            geolocate_ip(ip)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["2", "02"]:
            phone = input("[*] Enter Phone Number (e.g. +90xxx): ").strip()
            phone_recon(phone)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["3", "03"]:
            user = input("[*] Enter Username: ").strip()
            username_recon(user)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["4", "04"]:
            img_path = input("[*] Enter Image Path (e.g. C:\\Photos\\target.jpg): ").strip()
            img_path = img_path.strip('"').strip("'")
            exif_location_extractor(img_path)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["5", "05"]:
            break

def network_infra_menu():
    while True:
        clear_screen()
        print_header()
        print(f"{C}==== [ SUB-MENU: NETWORK & INFRA ] ===={W}\n")
        print(f"{R}[01]{W} Subdomain Scanner     {R}[02]{W} DNS Zone Lookup       {R}[03]{W} HTTP Header Grabber")
        print(f"{R}[04]{W} Quick Port Scanner    {R}[05]{W} WHOIS Domain Lookup   {R}[06]{W} Reverse DNS Lookup")
        print(f"{R}[07]{W} <-- Back to Main Menu")
        
        choice = input(f"\n{Y}[?] Select a network tool: {W}").strip()
        if choice in ["1", "01"]:
            domain = input("[*] Enter Domain (e.g. site.com): ").strip()
            subdomain_scanner(domain)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["2", "02"]:
            domain = input("[*] Enter Domain: ").strip()
            dns_lookup(domain)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["3", "03"]:
            domain = input("[*] Enter Target Domain: ").strip()
            http_header_grab(domain)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["4", "04"]:
            target = input("[*] Enter Target Host/Domain: ").strip()
            quick_port_scan(target)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["5", "05"]:
            domain = input("[*] Enter Domain: ").strip()
            whois_lookup(domain)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["6", "06"]:
            ip = input("[*] Enter Target IP: ").strip()
            reverse_dns(ip)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["7", "07"]:
            break

def hardware_recon_menu():
    while True:
        clear_screen()
        print_header()
        print(f"{C}==== [ SUB-MENU: HARDWARE RECON ] ===={W}\n")
        print(f"{R}[01]{W} MAC Address Lookup            {R}[02]{W} Wi-Fi Recon / SSID Analyzer")
        print(f"{R}[03]{W} <-- Back to Main Menu")
        
        choice = input(f"\n{Y}[?] Select a hardware tool: {W}").strip()
        if choice in ["1", "01"]:
            mac = input("[*] Enter MAC Address: ").strip()
            mac_lookup(mac)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["2", "02"]:
            target = input("[*] Enter MAC Address or SSID name: ").strip()
            wifi_recon(target)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["3", "03"]:
            break

def news_menu():
    while True:
        clear_screen()
        print_header()
        print(f"{O}==== [ SUB-MENU: ! NEWS (v1.2.1 FEATURES) ] ===={W}\n")
        print(f"{O}[01]{W} Data Breach Scanner     {O}[02]{W} Anti-OSINT (Image EXIF Cleaner)")
        print(f"{O}[03]{W} Email OSINT Detective   {O}[04]{W} Leak OSINT Analytics")
        print(f"{O}[05]{W} Hash Analyzer & Crack   {O}[06]{W} Web Vuln Quick Scanner")
        print(f"{O}[07]{W} Doc Metadata Cleaner    {O}[08]{W} URL Analyzer & SSL Certs")
        print(f"{O}[09]{W} <-- Back to Main Menu")
        
        choice = input(f"\n{Y}[?] Select a feature: {W}").strip()
        if choice in ["1", "01"]:
            email = input("[*] Enter Target Email: ").strip()
            data_breach_lookup(email)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["2", "02"]:
            img_path = input("[*] Enter Image Path to Clean (e.g. C:\\photo.jpg): ").strip()
            metadata_cleaner(img_path.strip('"').strip("'"))
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["3", "03"]:
            email = input("[*] Enter Target Email: ").strip()
            email_osint(email)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["4", "04"]:
            term = input("[*] Enter Target Email/Query for Leak Intel: ").strip()
            leak_osint_search(term)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["5", "05"]:
            h = input("[*] Enter Hash string: ").strip()
            hash_analyzer(h)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["6", "06"]:
            d = input("[*] Enter Web Domain to Scan: ").strip()
            web_vulnerability_scanner(d)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["7", "07"]:
            print(f"\n{C}[*] Document Metadata Cleaner (PDF/DOCX - Defense & Anti-OSINT){W}")
            print(f"    - Ideal for journalists, researchers, and privacy-focused users.")
            print(f"    - Strips author names, company info, and modification timestamps.\n")
            p = input("[*] Enter PDF or DOCX file path: ").strip()
            doc_metadata_cleaner(p.strip('"').strip("'"))
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["8", "08"]:
            u = input("[*] Enter URL to Analyze (Redirects/SSL): ").strip()
            url_analyzer(u)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["9", "09"]:
            break

def interactive_menu():
    while True:
        clear_screen()
        print_header()
        
        print(f"{R}[01]{W} OSINT Searchers               {R}[02]{W} Network & Infra")
        print(f"{R}[03]{W} Hardware Recon                {O}[04] ! NEWS (New Features){W}")
        print(f"{R}[05]{W} Exit Framework")
        
        choice = input(f"\n{Y}[?] Enter Category Code: {W}").strip()
        
        if choice in ["1", "01"]:
            osint_searchers_menu()
        elif choice in ["2", "02"]:
            network_infra_menu()
        elif choice in ["3", "03"]:
            hardware_recon_menu()
        elif choice in ["4", "04"]:
            news_menu()
        elif choice in ["5", "05"]:
            print(f"{Y}[*] Shutting down framework... Reports saved.{W}")
            sys.exit(0)
        else:
            print(f"{R}[-] Invalid Core Category.{W}")
            input(f"\n{C}Press Enter to refresh...{W}")

def main():
    if len(sys.argv) > 1:
        print_header()
        parser = argparse.ArgumentParser(description="FORSAKEN TOOL v1.2.1 - Advanced OSINT")
        parser.add_argument("-g", "--geo", type=str)
        parser.add_argument("-p", "--phone", type=str)
        parser.add_argument("-u", "--user", type=str)
        args = parser.parse_args()
        if args.geo: geolocate_ip(args.geo)
        elif args.phone: phone_recon(args.phone)
        elif args.user: username_recon(args.user)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
