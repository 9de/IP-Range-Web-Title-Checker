import requests
from bs4 import BeautifulSoup

def get_html_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string
            return title
        else:
            print(f"Failed to fetch HTML from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def check_ip_range(start_ip, end_ip):
    start = ip_to_int(start_ip)
    end = ip_to_int(end_ip)
    for ip_int in range(start, end + 1):
        ip = int_to_ip(ip_int)
        for port in [80, 443]:
            check_ip_and_port(ip, port)

def ip_to_int(ip):
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

def int_to_ip(ip_int):
    return '.'.join(str((ip_int >> i) & 0xFF) for i in (24, 16, 8, 0))

def check_ip_and_port(ip, port):
    urls = [f"http://{ip}:{port}", f"https://{ip}:{port}"]
    for url in urls:
        title = get_html_title(url)
        if title:
            print(f"Title for {url}: {title}")
            # Save the title to a file or database here if needed
        else:
            print(f"No title found for {url}")

# Example usage
start_ip = "162.19.0.0"
end_ip = "162.19.255.255"
check_ip_range(start_ip, end_ip)
