# Proxy Checker Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Proxy Checker Tool is designed to help you validate proxy servers. It allows you to check proxies from a file or a single proxy URL and determines its status and latency. This tool also provides a convenient way to interrupt the process if needed.

## Features

- Validate proxy servers.
- Support for different proxy types (http, https, socks4, socks5).
- Calculate and display latency of each proxy.
- User-friendly interruption by pressing 'q'.
- Color-coded output for easy status identification.

## Installation

To install this tool, you need to have Python 3.8 or above installed on your machine. Then, follow these steps:

1. Clone this repository:
    ```sh
    https://github.com/AmaniToamaWebDevelp1/proxychecker.git
    cd proxychecker
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command-line Arguments

- `-t`, `--txt`: Path to a text file containing proxy URLs, one per line.
- `-s`, `--single`: A single proxy URL to be checked immediately.
- `-p`, `--protocol`: Protocol to use with the single proxy (e.g., socks4), if not specified, it will be auto-detected.

### Running the Tool

Check proxies from a file:
```sh
python proxychecker.py -t path/to/proxyfile.txt
```

Check a single proxy:
```sh
python proxychecker.py -s http://10.20.200.13:80
```

Check a single proxy with a specified protocol:
```sh
python proxychecker.py -s socks5://10.20.200.13:1080 -p socks5
```

### Interrupting the Process

While checking proxies from a file, you can interrupt the process by pressing 'q' and then [Enter].

## Examples

Checking proxies from a file:
```sh
python proxychecker.py -t proxies.txt
```

Checking a single HTTP proxy:
```sh
python proxychecker.py -s http://10.20.200.13:80
```

Checking a single SOCKS5 proxy with auto-detection:
```sh
python proxychecker.py -s socks5://10.20.200.13:1080
```

Checking a single proxy with a specified protocol:
```sh
python proxychecker.py -s 10.20.200.13:1080 -p socks5
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed with ❤️ by Amani Toama
