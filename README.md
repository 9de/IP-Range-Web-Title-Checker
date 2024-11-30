# IP Range Scanner

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Interactive Mode](#interactive-mode)
  - [Configuration Options](#configuration-options)
- [Output](#output)
- [Examples](#examples)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Technical Documentation](#technical-documentation)

## Overview

IP Range Scanner is a powerful Python tool designed to scan ranges of IP addresses for web servers and collect their HTML titles. It supports concurrent scanning, multiple protocols (HTTP/HTTPS), custom port configurations, and provides comprehensive logging and CSV export capabilities.

## Features

- **Concurrent Scanning**: Utilizes multi-threading for efficient scanning of large IP ranges
- **Protocol Support**: Handles both HTTP and HTTPS protocols
- **Flexible Input**: Supports both command-line arguments and interactive input
- **Comprehensive Logging**: Detailed logging with both file and console output
- **Data Export**: Automatic CSV export of scan results
- **Input Validation**: Robust IP address and range validation
- **Configurable Settings**: Customizable timeout, worker threads, and ports
- **Error Handling**: Comprehensive error handling and graceful exits

## Requirements

- Python 3.7+
- Required packages:
  ```
  requests>=2.26.0
  beautifulsoup4>=4.9.3
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/9de/IP-Range-Web-Title-Checker.git
   cd ip-scanner
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```bash
python ip_scanner.py --start-ip START_IP --end-ip END_IP [OPTIONS]
```

### Interactive Mode

Simply run:
```bash
python ip_scanner.py
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--start-ip` | Starting IP address | Required |
| `--end-ip` | Ending IP address | Required |
| `--ports` | Ports to scan (space-separated) | 80 443 |
| `--timeout` | Request timeout in seconds | 5 |
| `--workers` | Number of concurrent workers | 10 |
| `--output` | Output CSV filename | scan_results_[timestamp].csv |

## Output

### Log Files
- Location: `scan_[timestamp].log`
- Format: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

### CSV Export
- Location: `scan_results_[timestamp].csv`
- Columns:
  - IP Address
  - URL
  - HTML Title

## Examples

1. Basic scan with default options:
   ```bash
   python ip_scanner.py --start-ip 192.168.1.1 --end-ip 192.168.1.255
   ```

2. Custom port scan:
   ```bash
   python ip_scanner.py --start-ip 10.0.0.1 --end-ip 10.0.0.100 --ports 80 8080 8443
   ```

3. Adjusted performance settings:
   ```bash
   python ip_scanner.py --start-ip 172.16.0.1 --end-ip 172.16.255.255 --timeout 3 --workers 20
   ```

## Security Considerations

1. **Network Policies**: Ensure compliance with network policies before scanning
2. **Rate Limiting**: Be aware of potential rate limiting on target networks
3. **Legal Implications**: Obtain necessary permissions before scanning non-owned networks
4. **SSL Verification**: Default SSL verification is enabled for security

## Troubleshooting

### Common Issues

1. **Connection Timeouts**
   - Increase timeout value using `--timeout`
   - Reduce number of workers using `--workers`

2. **Memory Issues**
   - Reduce the IP range size
   - Decrease number of concurrent workers

3. **Permission Errors**
   - Ensure write permissions for log and CSV files
   - Run with appropriate privileges

### Debug Mode

Set environment variable for detailed logging:
```bash
export IP_SCANNER_DEBUG=1  # On Windows: set IP_SCANNER_DEBUG=1
```

## Technical Documentation

### Class Structure

#### IPScanner

Main class handling the scanning operations.

```python
class IPScanner:
    def __init__(self, timeout: int = 5, max_workers: int = 10)
    def setup_logging(self)
    def get_html_title(self, url: str) -> Optional[str]
    def validate_ip_range(self, start_ip: str, end_ip: str) -> bool
    def scan_ip(self, ip: str, ports: List[int]) -> List[Tuple[str, str, str]]
    def scan_ip_range(self, start_ip: str, end_ip: str, ports: List[int]) -> List[Tuple[str, str, str]]
    def save_results(self, results: List[Tuple[str, str, str]], filename: str)
```

### Data Flow

1. User input validation
2. IP range conversion
3. Concurrent scanning
4. Result collection
5. Data export

### Performance Optimization

- Thread pool for concurrent scanning
- Configurable timeout and worker count
- Efficient IP address handling
- Minimal memory footprint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Coding Standards

- Follow PEP 8 guidelines
- Include type hints
- Add unit tests for new features
- Update documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool is provided for educational and legitimate network administration purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

## Support

For bug reports and feature requests, please use the GitHub issue tracker.

For questions and discussions:
- GitHub Discussions
