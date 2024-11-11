import requests
import sys
from colorama import Fore, init
import pyfiglet
import os
from concurrent.futures import ThreadPoolExecutor
import time
os.system('cls' if os.name == 'nt' else 'clear')
def banner():
    print("""
    _____________________________________________________
   |                                                     |
   |                  Simple Fuzzer Tool                 |
   |             Usage: python3 fuzzer.py <url>          |
   |      Example: fuzzer.py http://example.com/FUZZ     |
   |                                                     |
   |_____________________________________________________|
    """)

def read_wordlist(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"[!] Wordlist {filename} not found")
        sys.exit(1)

class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.current = 0
        self.start_time = time.time()
        self.found_urls = []
        # Print initial progress line
        print("\nProgress: 0.00% (0/{}) - Elapsed time: 0.00s".format(total))

    def update(self):
        self.current += 1
        elapsed_time = time.time() - self.start_time
        progress = (self.current / self.total) * 100
        # Move cursor up one line and clear it
        sys.stdout.write('\033[F\033[K')
        sys.stdout.write(f"Progress: {progress:.2f}% ({self.current}/{self.total}) - Elapsed time: {elapsed_time:.2f}s\n")
        sys.stdout.flush()

    def add_found(self, status, url):
        self.found_urls.append((status, url))

    def print_results(self):
        print("\nFound URLs:")
        for status, url in self.found_urls:
            if status == 200:
                print(f"{Fore.GREEN}[{status}] {url}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[{status}] {url}{Fore.RESET}")

def make_request(url, word, progress):
    target = url.replace('FUZZ', word)
    try:
        response = requests.get(target, timeout=5)
        if response.status_code != 404:
            progress.add_found(response.status_code, target)
        progress.update()
    except:
        progress.update()
        pass

def main():
    init()
    
    if len(sys.argv) != 2:
        banner()
        sys.exit(1)

    url = sys.argv[1]
    if 'FUZZ' not in url:
        print("[!] Please include FUZZ in the URL where you want to test")
        sys.exit(1)

    print(Fore.RED)
    pyfiglet.print_figlet("Asylum")
    print(Fore.RESET)
    
    print("[+] Starting fuzzer...")
    wordlist = read_wordlist('list.txt')
    total_words = len(wordlist)
    print(f"[+] Loaded {total_words} words from list.txt")

    progress = ProgressTracker(total_words)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, url, word, progress) for word in wordlist]
        for future in futures:
            future.result()
    
    progress.print_results()
    print("\n[+] Fuzzing completed!")

if __name__ == "__main__":
    main()

