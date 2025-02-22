import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os

def is_valid_url(url):
    """Check if a URL is valid."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def download_file(file_url, download_path):
    """Download a file from a URL."""
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        filename = os.path.basename(file_url)
        filepath = os.path.join(download_path, filename)
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"[+] Downloaded: {filepath}")
    except Exception as e:
        print(f"[-] Failed to download {file_url}: {e}")

def xss_scan(html_content):
    """Scan HTML content for potential XSS vulnerabilities."""
    patterns = [
        r'<script.*?>.*?</script>',
        r'on[a-zA-Z]+\s*=\s*".*?"',
        r'on[a-zA-Z]+\s*=\s*\'.*?\'',
        r'on[a-zA-Z]+\s*=\s*.*?>'
    ]
    print("\n[+] XSS Vulnerability Scan:")
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            print(f"[!] Potential XSS Found: {match}")

def web_crawler(start_url):
    """Crawl a website and extract links, images, and other resources."""
    if not is_valid_url(start_url):
        print("[-] Invalid or inaccessible URL. Please try again.")
        return

    print(f"[*] Crawling {start_url}...")
    try:
        response = requests.get(start_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all links
        print("\n[+] Links Found:")
        links = [urljoin(start_url, link.get('href')) for link in soup.find_all('a', href=True)]
        for link in links:
            print(f" - {link}")

        # Extract all images
        print("\n[+] Images Found:")
        images = [urljoin(start_url, img.get('src')) for img in soup.find_all('img', src=True)]
        for img in images:
            print(f" - {img}")

        # Extract CSS and JavaScript
        print("\n[+] CSS Files Found:")
        css_files = [urljoin(start_url, link.get('href')) for link in soup.find_all('link', rel="stylesheet")]
        for css in css_files:
            print(f" - {css}")

        print("\n[+] JavaScript Files Found:")
        js_files = [urljoin(start_url, script.get('src')) for script in soup.find_all('script', src=True)]
        for js in js_files:
            print(f" - {js}")

        # Extract other resources (e.g., XML, JSON, etc.)
        print("\n[+] Other Resources Found:")
        other_resources = [urljoin(start_url, link.get('href')) for link in soup.find_all('link', href=True) if link.get('rel') != "stylesheet"]
        other_resources += [urljoin(start_url, script.get('src')) for script in soup.find_all('script', src=True)]
        other_resources += [urljoin(start_url, source.get('src')) for source in soup.find_all(['source', 'track'], src=True)]
        for resource in other_resources:
            print(f" - {resource}")

        # Extract meta tags
        print("\n[+] Meta Information:")
        for meta in soup.find_all('meta'):
            meta_content = meta.get('content', 'No content')
            meta_name = meta.get('name', meta.get('property', 'Unnamed Meta'))
            print(f" - {meta_name}: {meta_content}")

        # Extract page title
        title = soup.title.string if soup.title else "No title found"
        print(f"\n[+] Page Title: {title}")

        # XSS Scan
        xss_scan(response.text)

        # Ask user for download options
        download_path = "downloads"
        os.makedirs(download_path, exist_ok=True)

        print("\n[?] Do you want to download all resources (Images, CSS, JavaScript, Other Resources)? (Y/N)")
        choice = input().strip().lower()
        if choice == 'y':
            for file_list in [images, css_files, js_files, other_resources]:
                for file_url in file_list:
                    download_file(file_url, download_path)

    except requests.exceptions.RequestException as e:
        print(f"[-] An error occurred: {e}")

def main():
    print("[ Web Crawler ]")
    start_url = input("Enter the starting URL: ").strip()
    web_crawler(start_url)

if __name__ == "__main__":
    main()