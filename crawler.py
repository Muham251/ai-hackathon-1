import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urljoin, urlparse

def crawl(url, visited, content_map):
    if url in visited:
        return
    
    print(f"Crawling: {url}")
    visited.add(url)
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return
    
    # Extract main content using trafilatura
    content = trafilatura.extract(response.content)
    if content:
        content_map[url] = content
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        joined_url = urljoin(url, href)
        
        # Parse the joined URL to check the domain
        parsed_url = urlparse(joined_url)
        
        # Only crawl URLs from the same domain
        if parsed_url.netloc == urlparse(url).netloc:
            crawl(joined_url, visited, content_map)

if __name__ == '__main__':
    start_url = "https://Muham251.github.io/ai-hackathon-1/"
    visited_urls = set()
    crawled_content = {}
    crawl(start_url, visited_urls, crawled_content)
    
    # Save the crawled content to a file
    with open("crawled_content.txt", "w", encoding="utf-8") as f:
        for url, content in crawled_content.items():
            f.write(f"URL: {url}\n")
            f.write(f"Content:\n{content}\n")
            f.write("-" * 80 + "\n")
            
    print("Crawling finished. Content saved to crawled_content.txt")
