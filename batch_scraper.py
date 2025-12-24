import os
import sys
from medium_scraper import MediumScraper, load_urls_from_file

def split_into_batches(urls, batch_size=1000):
    for i in range(0, len(urls), batch_size):
        yield urls[i:i + batch_size]

def batch_scrape(input_file, output_file='scrapping_results.csv', batch_size=1000, delay=1.0):
    print(f"Loading URLs from {input_file}...")
    urls = load_urls_from_file(input_file)
    total_urls = len(urls)
    print(f"Loaded {total_urls} URLs")
    
    scraper = MediumScraper(delay=delay)
    
    batch_num = 1
    total_batches = (total_urls + batch_size - 1) // batch_size
    
    for batch in split_into_batches(urls, batch_size):
        print(f"\n{'='*60}")
        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} URLs)")
        print(f"{'='*60}")
        
        scraper.scrape_urls(batch, output_file)
        
        batch_num += 1
        
        print(f"Progress: {min(batch_num * batch_size, total_urls)}/{total_urls} URLs processed")
    
    print(f"\n{'='*60}")
    print(f"All batches completed! Results saved to {output_file}")
    print(f"{'='*60}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch scrape Medium articles')
    parser.add_argument('--input', type=str, required=True, help='Input file with URLs')
    parser.add_argument('--output', type=str, default='scrapping_results.csv', help='Output CSV file')
    parser.add_argument('--batch-size', type=int, default=1000, help='URLs per batch')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    batch_scrape(args.input, args.output, args.batch_size, args.delay)
