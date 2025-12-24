# Medium Article Scraper and Search API

**Note: This project uses a sample size of 1,000 URLs for demonstration purposes.**

This project consists of two parts:
- **Part A**: A Python script to scrape Medium articles and extract comprehensive data
- **Part B**: A Flask API to search for similar articles based on text/keywords

## Part A: Medium Article Scraper

### Features

The scraper extracts the following data from Medium articles:
- Title
- Subtitle
- Text content
- Number of images
- Image URLs
- Number of external links
- Author Name
- Author URL
- Claps (likes)
- Reading time
- Keywords

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Scrape from a file containing URLs

Create a text file (`urls.txt`) with one URL per line:
```
https://medium.com/@user/article-1
https://medium.com/@user/article-2
https://towardsdatascience.com/article-3
```

Then run:
```bash
python medium_scraper.py --urls urls.txt --output scrapping_results.csv
```

#### Option 2: Scrape a single URL

```bash
python medium_scraper.py --url https://medium.com/@user/article-1 --output scrapping_results.csv
```

#### Option 3: Interactive mode

```bash
python medium_scraper.py
# Then paste URLs one by one, press Enter twice when done
```

#### Command-line Arguments

- `--urls`: Path to file containing URLs (one per line)
- `--url`: Single URL to scrape
- `--output`: Output CSV file path (default: `scrapping_results.csv`)
- `--delay`: Delay between requests in seconds (default: 1.0)

### Example

```bash
# Scrape 100 URLs with 2 second delay between requests
python medium_scraper.py --urls medium_urls.txt --output scrapping_results.csv --delay 2.0
```

### Output Format

The scraper generates a CSV file (`scrapping_results.csv`) with the following columns:
- `url`: Article URL
- `title`: Article title
- `subtitle`: Article subtitle
- `text`: Full article text
- `num_images`: Number of images in the article
- `image_urls`: Semicolon-separated list of image URLs
- `num_external_links`: Number of external links
- `author_name`: Author's name
- `author_url`: Author's profile URL
- `claps`: Number of claps (likes)
- `reading_time`: Reading time in minutes
- `keywords`: Extracted keywords

## Part B: Search API

### Features

- Search for similar articles based on text or keywords
- Returns top 10 most clapped similar articles
- Uses TF-IDF vectorization and cosine similarity for matching
- RESTful API with JSON responses

### Local Setup

1. Ensure you have scraped data in `scrapping_results.csv`

2. Run the API:
```bash
python api.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "data_loaded": true,
  "articles_count": 1000
}
```

#### 2. Search Articles

**GET Request:**
```bash
GET /search?query=machine+learning&top_n=10
```

**POST Request:**
```bash
POST /search
Content-Type: application/json

{
  "query": "machine learning",
  "top_n": 10
}
```

**Response:**
```json
{
  "query": "machine learning",
  "count": 10,
  "results": [
    {
      "url": "https://medium.com/@user/article-1",
      "title": "Introduction to Machine Learning",
      "claps": 5000,
      "similarity_score": 0.85
    },
    ...
  ]
}
```

#### 3. API Documentation
```bash
GET /
```

Returns API documentation and usage examples.

### Deployment to Free Hosting Platforms

#### Option 1: Render.com

1. Create a new account on [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn api:app`
6. Add environment variable `CSV_FILE=scrapping_results.csv` (if needed)
7. Deploy!

#### Option 2: Railway.app

1. Create a new account on [Railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository or upload files
4. Railway will auto-detect Python and install dependencies
5. Set start command: `gunicorn api:app`
6. Deploy!

#### Option 3: Heroku (Free tier discontinued, but still works)

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. The `Procfile` will automatically be used

#### Option 4: PythonAnywhere

1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your files via the web interface
3. Create a new web app
4. Set the source code path
5. Configure WSGI file to point to `api.py`
6. Reload the web app

### Important Notes for Deployment

1. **Upload CSV file**: Make sure to upload `scrapping_results.csv` to your hosting platform
2. **Environment Variables**: Some platforms may require setting `PORT` environment variable
3. **File Paths**: The API looks for `scrapping_results.csv` in the same directory. Adjust if needed using the `CSV_FILE` environment variable

### Project Structure

```
Uni/
├── medium_scraper.py      # Part A: Scraper script
├── api.py                  # Part B: Search API
├── requirements.txt        # Python dependencies
├── Procfile               # For Heroku/Render deployment
├── runtime.txt            # Python version specification
├── .gitignore             # Git ignore file
├── README.md              # This file
└── scrapping_results.csv  # Output file (generated after scraping)
```

### Troubleshooting

#### Scraper Issues

1. **Rate Limiting**: If you encounter rate limiting, increase the `--delay` parameter
2. **Missing Data**: Some articles may have missing fields. The scraper handles this gracefully
3. **Network Errors**: Ensure stable internet connection and retry failed URLs

#### API Issues

1. **Data Not Loaded**: Ensure `scrapping_results.csv` exists and is in the correct location
2. **No Results**: Try different search queries or check if your CSV has data
3. **Memory Issues**: For very large datasets (>100k articles), consider using a database instead of loading everything into memory

### Performance Tips

1. **Scraping**: Use appropriate delays (1-2 seconds) to avoid being blocked
2. **Batch Processing**: For large datasets (e.g., 1,000 URLs), consider running the scraper in batches
3. **API**: The API loads all data into memory. For production with large datasets, consider using a database (PostgreSQL, MongoDB) with vector search capabilities

### Example Workflow

1. **Scrape Articles**:
```bash
python medium_scraper.py --urls medium_urls.txt --output scrapping_results.csv --delay 1.5
```

2. **Test API Locally**:
```bash
python api.py
# In another terminal:
curl "http://localhost:5000/search?query=data+science"
```

3. **Deploy API**:
   - Push to GitHub
   - Deploy to Render/Railway/Heroku
   - Upload `scrapping_results.csv` to the hosting platform

### License

This project is for educational purposes.

### Support

For issues or questions, please check:
- Ensure all dependencies are installed
- Check that URLs are valid Medium article URLs
- Verify CSV file format and location
- Check API logs for error messages


