import requests
from bs4 import BeautifulSoup
import ipaddress
import concurrent.futures
import argparse
import logging
from typing import Optional, List, Tuple
import csv
from datetime import datetime
import socket
import sys

class IPScanner:
    def __init__(self, timeout: int = 5, max_workers: int = 10):
        self.timeout = timeout
        self.max_workers = max_workers
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_html_title(self, url: str) -> Optional[str]:
        """Fetch and return the HTML title from a given URL"""
        try:
            response = requests.get(url, timeout=self.timeout, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.title.string.strip() if soup.title else None
        except requests.RequestException as e:
            self.logger.debug(f"Failed to fetch {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.debug(f"Error processing {url}: {str(e)}")
            return None

    def validate_ip_range(self, start_ip: str, end_ip: str) -> bool:
        """Validate if the IP range is valid"""
        try:
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)
            if start > end:
                raise ValueError("Start IP must be less than or equal to End IP")
            return True
        except Exception as e:
            self.logger.error(f"Invalid IP range: {str(e)}")
            return False

    def scan_ip(self, ip: str, ports: List[int]) -> List[Tuple[str, str, str]]:
        """Scan a single IP address across specified ports"""
        results = []
        for port in ports:
            protocols = ['http', 'https'] if port == 443 else ['http']
            for protocol in protocols:
                url = f"{protocol}://{ip}:{port}"
                title = self.get_html_title(url)
                if title:
                    results.append((ip, url, title))
                    self.logger.info(f"Found title for {url}: {title}")
        return results

    def scan_ip_range(self, start_ip: str, end_ip: str, ports: List[int]) -> List[Tuple[str, str, str]]:
        """Scan a range of IP addresses using multiple threads"""
        if not self.validate_ip_range(start_ip, end_ip):
            return []

        start = int(ipaddress.IPv4Address(start_ip))
        end = int(ipaddress.IPv4Address(end_ip))
        all_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_ip = {
                executor.submit(
                    self.scan_ip, 
                    str(ipaddress.IPv4Address(ip)), 
                    ports
                ): ip for ip in range(start, end + 1)
            }

            for future in concurrent.futures.as_completed(future_to_ip):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    self.logger.error(f"Error scanning IP: {str(e)}")

        return all_results

    def save_results(self, results: List[Tuple[str, str, str]], filename: str):
        """Save scan results to a CSV file"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['IP', 'URL', 'Title'])
                writer.writerows(results)
            self.logger.info(f"Results saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Scan IP ranges for web servers and their titles')
    parser.add_argument('--start-ip', type=str, help='Starting IP address')
    parser.add_argument('--end-ip', type=str, help='Ending IP address')
    parser.add_argument('--ports', type=int, nargs='+', default=[80, 443], help='Ports to scan')
    parser.add_argument('--timeout', type=int, default=5, help='Request timeout in seconds')
    parser.add_argument('--workers', type=int, default=10, help='Number of worker threads')
    parser.add_argument('--output', type=str, default=f'scan_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                        help='Output CSV file name')

    args = parser.parse_args()

    # If arguments aren't provided, ask for them interactively
    if not args.start_ip:
        args.start_ip = input("Enter starting IP address: ")
    if not args.end_ip:
        args.end_ip = input("Enter ending IP address: ")

    scanner = IPScanner(timeout=args.timeout, max_workers=args.workers)
    results = scanner.scan_ip_range(args.start_ip, args.end_ip, args.ports)
    scanner.save_results(results, args.output)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(1)
