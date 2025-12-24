from medium_scraper import MediumScraper
import sys

def extract_urls_from_rss_feeds(rss_urls, output_file='urls.txt', max_urls=1000):
    scraper = MediumScraper()
    all_urls = []
    
    print(f"Extracting article URLs from RSS feeds...")
    print(f"Sample size: {max_urls} URLs")
    print("=" * 60)
    
    for rss_url in rss_urls:
        urls = scraper.extract_article_urls_from_rss(rss_url)
        all_urls.extend(urls)
        
        if len(all_urls) >= max_urls:
            all_urls = all_urls[:max_urls]
            print(f"\nReached sample size limit of {max_urls} URLs")
            break
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in all_urls:
            f.write(url + '\n')
    
    print(f"\n{'='*60}")
    print(f"Saved {len(all_urls)} article URLs to {output_file}")
    print(f"Sample size: {len(all_urls)} URLs")
    print(f"{'='*60}")
    print(f"\nNow you can scrape these articles:")
    print(f"python medium_scraper.py --urls {output_file} --output scrapping_results.csv --delay 2.0")

if __name__ == '__main__':
    rss_feeds = [
        'https://medium.com/feed/tag/technology',
        'https://medium.com/feed/tag/programming',
        'https://medium.com/feed/tag/data-science',
        'https://medium.com/feed/tag/machine-learning',
        'https://medium.com/feed/tag/python'
    ]
    
    max_urls = 1000
    
    if len(sys.argv) > 1:
        rss_feeds = sys.argv[1:]
    
    extract_urls_from_rss_feeds(rss_feeds, 'urls.txt', max_urls)
