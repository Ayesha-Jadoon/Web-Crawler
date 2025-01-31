from collections import deque
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import threading
import hashlib

# Thread-safe set for visited URLs
visited = set()
visited_lock = threading.Lock()

# Set for storing content hashes to detect duplicates
content_hashes = set()
content_hashes_lock = threading.Lock()

def fetch_page(url):
    """Fetch the HTML content of a page."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return url, response.text
    except requests.exceptions.RequestException:
        return url, None

def extract_links(html, base_url):
    """Extract all hyperlinks from the page."""
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    return [urljoin(base_url, a_tag['href']) for a_tag in soup.find_all('a', href=True)]

def extract_content(html, url):
    """Extract specific content (title, headings, paragraphs, images) from the page."""
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "url": url,
        "title": soup.title.string if soup.title else None,
        "headings": [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
        "paragraphs": [p.get_text() for p in soup.find_all('p')],
        "images": [img['src'] for img in soup.find_all('img', src=True)]
    }

def normalize_url(url):
    """Normalize URL to avoid duplicates."""
    parsed = urlparse(url)
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, None, None, None))
    return clean_url.rstrip('/')

def hash_content(content):
    """Generate a hash for the page content."""
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

def check_robots(base_url, url):
    """Check if crawling is allowed by robots.txt."""
    try:
        parsed_base = urlparse(base_url)
        robots_url = f"{parsed_base.scheme}://{parsed_base.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except Exception:
        return True

def crawl(start_url, max_depth=1):
    """Perform BFS-based web crawling up to max_depth."""
    queue = deque([(0, start_url)])  # (depth, url)
    crawled_data = []
    total_links_found = 0
    
    parsed_start = urlparse(start_url)
    base_domain = f"{parsed_start.scheme}://{parsed_start.netloc}"
    domain_name = parsed_start.netloc.replace("www.", "")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}

        while queue:
            depth, current_url = queue.popleft()
            normalized_url = normalize_url(current_url)

            with visited_lock:
                if normalized_url in visited or depth > max_depth:
                    continue
                visited.add(normalized_url)

            if not check_robots(base_domain, current_url):
                print(f"[SKIP] {current_url} (Blocked by robots.txt)")
                continue

            print(f"[Crawling] {current_url}")
            future = executor.submit(fetch_page, current_url)
            futures[future] = (depth, current_url)

            for future in as_completed(futures):
                depth, url = futures[future]
                del futures[future]

                url, html = future.result()
                if html:
                    content = extract_content(html, url)
                    if content:
                        content_hash = hash_content(content)

                        with content_hashes_lock:
                            if content_hash in content_hashes:
                                print(f"[Duplicate] {url} (Skipped)")
                                continue
                            content_hashes.add(content_hash)

                        crawled_data.append(content)

                    links = extract_links(html, url)
                    total_links_found += len(links)
                    for link in links:
                        normalized_link = normalize_url(link)
                        parsed_link = urlparse(normalized_link)
                        if parsed_link.netloc == parsed_start.netloc:
                            with visited_lock:
                                if normalized_link not in visited and depth + 1 <= max_depth:
                                    queue.append((depth + 1, normalized_link))

    # Save only non-blocked pages to JSON
    if crawled_data:
        json_filename = f"output/{domain_name}_crawled_data.json" 
        with open(json_filename, "w") as f:
            json.dump(crawled_data, f, indent=4)
        print(f"\n[Crawl Complete] Data saved in: {json_filename}")
    else:
        print("\nNo data to save as all pages were blocked by robots.txt or empty.")

    print(f"\nTotal URLs Crawled: {len(crawled_data)}")
    print(f"Total Links Extracted: {total_links_found}")

if __name__ == "__main__":
    start_url = input("Enter the website URL to crawl: ").strip()
    if not start_url.startswith(('http://', 'https://')):
        print("Invalid URL. Please make sure it starts with 'http://' or 'https://'.")
    else:
        crawl(start_url, max_depth=1)
