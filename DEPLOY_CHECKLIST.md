# Render Deployment Checklist

## Pre-Deployment

- [x] All comments removed from Python files
- [ ] CSV file ready (scrapping_results.csv with 1,000 articles)
- [ ] Procfile exists: `web: gunicorn api:app`
- [ ] requirements.txt has all dependencies
- [ ] runtime.txt specifies Python version

## Deployment Steps

### 1. GitHub Setup
```bash
cd Uni
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Render Setup
1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect GitHub
5. Select your repository

### 3. Render Configuration
- **Name**: medium-search-api
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn api:app`
- **Plan**: Free

### 4. Upload CSV
After first deployment, upload CSV file:
- Option A: Use Render Shell
  - Go to your service → Shell tab
  - Use `echo` or file upload to create scrapping_results.csv
- Option B: Force add to Git (if needed)
  ```bash
  git add -f scrapping_results.csv
  git commit -m "Add CSV data"
  git push
  ```
- Option C: Generate on Render
  - In Render Shell: `python generate_1000_articles.py`

### 5. Test
Your API will be at: `https://your-app-name.onrender.com`

Test:
```bash
curl https://your-app-name.onrender.com/health
curl "https://your-app-name.onrender.com/search?query=machine+learning"
```

## Files Needed for Deployment

- api.py
- requirements.txt
- Procfile
- runtime.txt
- scrapping_results.csv (upload after deployment)

## Notes

- Free tier spins down after 15 min inactivity
- First request after spin-down takes ~30 seconds
- CSV must be in same directory as api.py

