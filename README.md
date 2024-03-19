# IP Range Web Title Checker

This Python script allows you to check the HTML titles of web pages within a specified IP range. It utilizes the `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML content.

## How it Works

- The script converts the start and end IPs of a range into integers for iteration.
- It then iterates through each IP in the range and checks common ports (80 and 443) for HTTP and HTTPS connections respectively.
- For each IP and port combination, it fetches the HTML content and extracts the title using BeautifulSoup.
- If a title is found, it prints it out. Optionally, you can save the titles to a file or database.

## Usage

```python
start_ip = "162.19.0.0"
end_ip = "162.19.255.255"
check_ip_range(start_ip, end_ip)
```

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` library

## Installation

You can install the required libraries using pip:

```
pip install requests beautifulsoup4
```

## Example

```python
check_ip_range("193.19.0.0", "193.19.255.255")
```

## Author

Turki

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
