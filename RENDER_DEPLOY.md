# Deploy to Render.com

## Step 1: Prepare Your Code

1. Make sure all files are in the `Uni` folder
2. Ensure `scrapping_results.csv` exists (or generate it with `generate_1000_articles.py`)

## Step 2: Create GitHub Repository

1. Go to https://github.com and create a new repository
2. Initialize git in your Uni folder:
```bash
cd Uni
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your repository
5. Configure settings:
   - **Name**: medium-search-api (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app`
   - **Plan**: Free (or paid if you prefer)

## Step 4: Upload CSV File

After deployment:

1. Go to your service dashboard on Render
2. Click "Shell" tab
3. Upload `scrapping_results.csv`:
   ```bash
   # In Render shell, create the file or upload it
   # You can use: echo "your csv content" > scrapping_results.csv
   # Or use Render's file upload feature if available
   ```

Alternative: Add CSV to your GitHub repo and it will be deployed automatically.

## Step 5: Environment Variables (Optional)

In Render dashboard → Environment:
- `PORT`: Auto-set by Render
- `CSV_FILE`: scrapping_results.csv (if different name)

## Step 6: Test Your API

Once deployed, your API will be at:
`https://your-app-name.onrender.com`

Test it:
```bash
curl https://your-app-name.onrender.com/health
curl "https://your-app-name.onrender.com/search?query=machine+learning"
```

## Important Notes

- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- CSV file must be in the same directory as `api.py`
- Make sure `Procfile` exists with: `web: gunicorn api:app`

## Troubleshooting

- **Build fails**: Check `requirements.txt` is correct
- **API returns 500**: Check if CSV file exists and is uploaded
- **Slow response**: Normal on free tier after spin-down

