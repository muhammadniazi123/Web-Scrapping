import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import csv
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import logging
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MediumScraper:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Referer': 'https://www.google.com/'
        })
    
    def extract_article_urls_from_rss(self, rss_url: str) -> List[str]:
        try:
            logger.info(f"Extracting article URLs from RSS feed: {rss_url}")
            response = self.session.get(rss_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            urls = []
            
            for item in soup.find_all('item'):
                link = item.find('link')
                if link and link.text:
                    urls.append(link.text.strip())
            
            logger.info(f"Found {len(urls)} article URLs in RSS feed")
            return urls
            
        except Exception as e:
            logger.error(f"Error extracting URLs from RSS feed: {str(e)}")
            return []
    
    def extract_json_ld(self, soup: BeautifulSoup) -> Optional[Dict]:
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'BlogPosting':
                    return data
            except:
                continue
        return None
    
    def extract_article_data(self, url: str) -> Dict:
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result = {
                'url': url,
                'title': '',
                'subtitle': '',
                'text': '',
                'num_images': 0,
                'image_urls': '',
                'num_external_links': 0,
                'author_name': '',
                'author_url': '',
                'claps': 0,
                'reading_time': 0,
                'keywords': ''
            }
            
            json_ld = self.extract_json_ld(soup)
            
            if json_ld and json_ld.get('headline'):
                result['title'] = json_ld['headline']
            else:
                title_tag = soup.find('h1') or soup.find('title')
                if title_tag:
                    result['title'] = title_tag.get_text(strip=True)
            
            subtitle_tag = soup.find('h2', class_=re.compile('subtitle|deck')) or \
                          soup.find('div', class_=re.compile('subtitle'))
            if subtitle_tag:
                result['subtitle'] = subtitle_tag.get_text(strip=True)
            elif json_ld and json_ld.get('description'):
                result['subtitle'] = json_ld['description']
            
            if json_ld and json_ld.get('author'):
                author = json_ld['author']
                if isinstance(author, dict):
                    result['author_name'] = author.get('name', '')
                    result['author_url'] = author.get('url', '')
            
            if not result['author_name']:
                author_link = soup.find('a', class_=re.compile('author|writer'))
                if author_link:
                    result['author_name'] = author_link.get_text(strip=True)
                    result['author_url'] = author_link.get('href', '')
                    if result['author_url'] and not result['author_url'].startswith('http'):
                        result['author_url'] = urljoin('https://medium.com', result['author_url'])
            
            article_body = soup.find('article') or soup.find('div', class_=re.compile('post|article|content'))
            if not article_body:
                article_body = soup.find('main') or soup.find('div', id=re.compile('content|post'))
            
            if article_body:
                for script in article_body(["script", "style", "nav", "footer", "header"]):
                    script.decompose()
                
                paragraphs = article_body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                text_parts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                result['text'] = ' '.join(text_parts)
            
            images = []
            if article_body:
                img_tags = article_body.find_all('img')
            else:
                img_tags = soup.find_all('img')
            
            for img in img_tags:
                img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if img_url:
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = urljoin(url, img_url)
                    
                    if 'avatar' not in img_url.lower() and 'icon' not in img_url.lower():
                        images.append(img_url)
            
            result['num_images'] = len(images)
            result['image_urls'] = '; '.join(images[:50])
            
            external_links = []
            base_domain = urlparse(url).netloc
            if article_body:
                links = article_body.find_all('a', href=True)
            else:
                links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                if href:
                    if href.startswith('//'):
                        href = 'https:' + href
                    elif href.startswith('/'):
                        href = urljoin(url, href)
                    
                    link_domain = urlparse(href).netloc
                    if link_domain and link_domain != base_domain and link_domain != 'medium.com':
                        external_links.append(href)
            
            result['num_external_links'] = len(external_links)
            
            claps_elem = soup.find('button', class_=re.compile('clap|like')) or \
                        soup.find('div', class_=re.compile('clap'))
            if claps_elem:
                claps_text = claps_elem.get_text(strip=True)
                claps_match = re.search(r'(\d+[KkMm]?|\d+)', claps_text)
                if claps_match:
                    claps_str = claps_match.group(1)
                    if 'K' in claps_str.upper():
                        result['claps'] = int(float(claps_str.upper().replace('K', '')) * 1000)
                    elif 'M' in claps_str.upper():
                        result['claps'] = int(float(claps_str.upper().replace('M', '')) * 1000000)
                    else:
                        result['claps'] = int(claps_str)
            
            if result['claps'] == 0:
                claps_data = soup.find('button', attrs={'data-action': re.compile('clap')})
                if claps_data:
                    claps_text = claps_data.get_text(strip=True)
                    claps_match = re.search(r'(\d+)', claps_text)
                    if claps_match:
                        result['claps'] = int(claps_match.group(1))
            
            reading_time_elem = soup.find(string=re.compile(r'\d+\s*min\s*read', re.I))
            if reading_time_elem:
                time_match = re.search(r'(\d+)', reading_time_elem)
                if time_match:
                    result['reading_time'] = int(time_match.group(1))
            
            if result['reading_time'] == 0:
                reading_div = soup.find('div', class_=re.compile('reading|time'))
                if reading_div:
                    time_text = reading_div.get_text()
                    time_match = re.search(r'(\d+)', time_text)
                    if time_match:
                        result['reading_time'] = int(time_match.group(1))
            
            keywords_meta = soup.find('meta', attrs={'name': re.compile('keyword', re.I)})
            if keywords_meta:
                result['keywords'] = keywords_meta.get('content', '')
            
            if not result['keywords'] and result['text']:
                words = re.findall(r'\b[a-zA-Z]{4,}\b', result['text'].lower())
                word_freq = {}
                for word in words:
                    if word not in ['that', 'this', 'with', 'from', 'have', 'will', 'your', 'they', 'their']:
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
                result['keywords'] = ', '.join([word for word, _ in top_keywords])
            
            result['text'] = ' '.join(result['text'].split())
            
            logger.info(f"Successfully scraped: {result['title'][:50]}...")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return self._create_error_result(url, f"Request error: {str(e)}")
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return self._create_error_result(url, f"Error: {str(e)}")
    
    def _create_error_result(self, url: str, error_msg: str) -> Dict:
        return {
            'url': url,
            'title': '',
            'subtitle': '',
            'text': '',
            'num_images': 0,
            'image_urls': '',
            'num_external_links': 0,
            'author_name': '',
            'author_url': '',
            'claps': 0,
            'reading_time': 0,
            'keywords': '',
            'error': error_msg
        }
    
    def scrape_urls(self, urls: List[str], output_file: str = 'scrapping_results.csv') -> None:
        fieldnames = [
            'url', 'title', 'subtitle', 'text', 'num_images', 'image_urls',
            'num_external_links', 'author_name', 'author_url', 'claps',
            'reading_time', 'keywords'
        ]
        
        file_exists = False
        try:
            with open(output_file, 'r', encoding='utf-8'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            total = len(urls)
            for idx, url in enumerate(urls, 1):
                logger.info(f"Processing {idx}/{total}: {url}")
                result = self.extract_article_data(url)
                
                result_to_write = {k: v for k, v in result.items() if k in fieldnames}
                writer.writerow(result_to_write)
                
                if idx < total:
                    time.sleep(self.delay)
        
        logger.info(f"Scraping complete! Results saved to {output_file}")


def load_urls_from_file(file_path: str) -> List[str]:
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and url.startswith('http'):
                    urls.append(url)
        logger.info(f"Loaded {len(urls)} URLs from {file_path}")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    return urls


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape Medium articles')
    parser.add_argument('--urls', type=str, help='Path to file containing URLs (one per line)')
    parser.add_argument('--url', type=str, help='Single URL to scrape')
    parser.add_argument('--output', type=str, default='scrapping_results.csv', help='Output CSV file')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    scraper = MediumScraper(delay=args.delay)
    urls = []
    
    if args.urls:
        urls = load_urls_from_file(args.urls)
    elif args.url:
        urls = [args.url]
    else:
        print("Enter Medium URLs (one per line, press Enter twice to finish):")
        while True:
            url = input().strip()
            if not url:
                break
            if url.startswith('http'):
                urls.append(url)
    
    if not urls:
        print("No URLs provided. Exiting.")
        return
    
    scraper.scrape_urls(urls, args.output)


if __name__ == '__main__':
    main()
