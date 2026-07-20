import os
import sys
import subprocess
import argparse
import socket
from datetime import datetime

def auto_install(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
    except ImportError:
        print(f"[*] '{package_name}' bulunamadı. Arka planda sessizce kuruluyor, lütfen bekleyin...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            print(f"[+] '{package_name}' başarıyla kuruldu!")
        except Exception as e:
            print(f"[-] '{package_name}' kurulamadı: {e}\nLütfen manuel olarak 'pip install {package_name}' komutunu girin.")
            sys.exit(1)

auto_install("requests")
auto_install("phonenumbers")
auto_install("Pillow", "PIL")

import requests
import phonenumbers
from phonenumbers import geocoder, carrier
from PIL import Image, ExifTags

__version__ = "3.0.0"
__author__ = "By D3xt4r"

if os.name == 'nt':
    os.system('color 0c')

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
W = "\033[0m"
C = "\033[36m"

REPORT_FILE = "forsaken_report.txt"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def log_to_report(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_content = content.replace(R, "").replace(G, "").replace(Y, "").replace(W, "").replace(C, "")
    try:
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {clean_content}\n")
    except Exception:
        pass

def print_header():
    banner = f"""{R}
    ███████╗██████╗ ██████╗ ███████╗███████╗██╗  ██╗███████╗███╗   ██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██║ ██╔╝██╔════╝████╗  ██║
    █████╗  ██║   ██║██████╔╝███████╗█████╗  █████╔╝ █████╗  ██╔██╗ ██║
    ██╔══╝  ██║   ██║██╔══██╗╚════██║██╔══╝  ██╔═██╗ ██╔══╝  ██║╚██╗██║
    ██║     ╚██████╔╝██║  ██║███████║███████╗██║  ██╗███████╗██║ ╚████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
                                                                   
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

def osint_searchers_menu():
    while True:
        clear_screen()
        print_header()
        print(f"{C}==== [ SUB-MENU: OSINT SEARCHERS (SORGU) ] ===={W}\n")
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
        print(f"{C}==== [ SUB-MENU: NETWORK & INFRA (AĞ) ] ===={W}\n")
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
        print(f"{C}==== [ SUB-MENU: HARDWARE RECON (DONANIM) ] ===={W}\n")
        print(f"{R}[01]{W} MAC Address Lookup            {R}[02]{W} <-- Back to Main Menu")
        
        choice = input(f"\n{Y}[?] Select a hardware tool: {W}").strip()
        if choice in ["1", "01"]:
            mac = input("[*] Enter MAC Address: ").strip()
            mac_lookup(mac)
            input(f"\n{C}Press Enter to return...{W}")
        elif choice in ["2", "02"]:
            break

def interactive_menu():
    while True:
        clear_screen()
        print_header()
        
        print(f"{R}[01]{W} OSINT Searchers (Sorgu)       {R}[02]{W} Network & Infra (Ağ)")
        print(f"{R}[03]{W} Hardware Recon (Donanım)       {R}[04]{W} Exit Framework")
        
        choice = input(f"\n{Y}[?] Enter Category Code: {W}").strip()
        
        if choice in ["1", "01"]:
            osint_searchers_menu()
        elif choice in ["2", "02"]:
            network_infra_menu()
        elif choice in ["3", "03"]:
            hardware_recon_menu()
        elif choice in ["4", "04"]:
            print(f"{Y}[*] Shutting down framework... Reports saved.{W}")
            sys.exit(0)
        else:
            print(f"{R}[-] Invalid Core Category.{W}")
            input(f"\n{C}Press Enter to refresh...{W}")

def main():
    if len(sys.argv) > 1:
        print_header()
        parser = argparse.ArgumentParser(description="FORSAKEN TOOL v3.0 - Advanced OSINT")
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