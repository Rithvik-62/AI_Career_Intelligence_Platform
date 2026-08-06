# 🌐 AI Career Intelligence Platform V2.0 — Independent Deployment Guide

This guide provides step-by-step instructions to push this **Version 2.0** codebase to a **brand-new, completely independent GitHub repository** and deploy it as a **brand-new Streamlit Cloud application** — leaving all existing repositories and deployments 100% untouched.

---

## 🔒 Step 1: Create a Brand-New GitHub Repository

> ⚠️ **CRITICAL:** Do NOT push to or overwrite your existing GitHub repository. Create a completely new repository.

1. Open [GitHub](https://github.com/new) in your web browser.
2. Enter a **New Repository Name**:
   - Recommended: `AI-Career-Intelligence-Platform-V2`
   - Alternative: `Career-Analytics-Platform-V2`
3. Description: `Production-Grade AI & ML Career Intelligence Platform V2.0 (Resume Extraction, Career Prediction, Skill Gap Analysis & Gemini AI)`
4. Visibility: Select **Public** (or **Private** if preferred).
5. **DO NOT** check "Initialize this repository with a README" (we already have a complete V2.0 `README.md`).
6. Click **Create repository**.

---

## 🚀 Step 2: Push Code to the New GitHub Repository

Run the following commands in your terminal inside your project directory (`AI_Career_Intelligence_Platform`):

```bash
# 1. Verify you are in the project folder
cd "d:\antigravity project\CLT_Mission\AI_Career_Intelligence_Platform"

# 2. Check current git status
git status

# 3. Create a fresh clean release branch or checkout main
git checkout -b main

# 4. Add all V2.0 files
git add .

# 5. Commit V2.0 Release
git commit -m "feat: AI Career Intelligence Platform V2.0 Production Release"

# 6. Link to your NEW GitHub Repository (replace YOUR-USERNAME and NEW-REPO-NAME)
git remote add origin-v2 https://github.com/YOUR-USERNAME/AI-Career-Intelligence-Platform-V2.git

# 7. Push V2.0 code to your NEW repository
git push -u origin-v2 main
```

---

## ☁️ Step 3: Connect & Deploy on Streamlit Cloud

1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click the **"Create app"** button (top right).
3. Select **"I already have an app"**.
4. Configure the deployment settings:
   - **Repository:** `YOUR-USERNAME/AI-Career-Intelligence-Platform-V2`
   - **Branch:** `main`
   - **Main file path:** `app/streamlit_app.py`
   - **App URL (optional custom subdomain):** `ai-career-intelligence-v2.streamlit.app`

---

## 🔑 Step 4: Configure Environment Secrets (Gemini 3.6 AI)

1. Before clicking Deploy, click **"Advanced settings..."** (or go to **App Settings -> Secrets** after creation).
2. Paste your Google Gemini API Key in TOML format:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourActualGeminiApiKeyHere..."
   ```
3. Click **Save** and then click **Deploy!**

---

## ✅ Step 5: Verify Your Live Independent Deployment

Once deployment completes (approx 1-2 minutes):

1. **Upload Resume**: Test uploading a sample PDF resume on the **Home Overview** page.
2. **Verify Extraction**: Confirm Name, Links (LinkedIn, GitHub), Education, Projects, and Courses render.
3. **Verify ML Predictions**: Check **ML Career Prediction** for top 5 ranked roles.
4. **Verify BI Dashboard**: Check interactive Plotly radar charts, gauges, and KPI cards.
5. **Verify PDF Export**: Download the executive career report PDF from the Dashboard.
6. **Verify Gemini AI**: Ask Aria in the sidebar chatbot or generate an AI Cover Letter.

---

## 🛠️ Step 6: Troubleshooting & Common Fixes

| Issue / Error | Cause | Instant Solution |
|:---|:---|:---|
| `ModuleNotFoundError: No module named 'pdfplumber'` | Missing dependency | Ensure `requirements.txt` is in the repository root directory. |
| `FileNotFoundError: models/career_model.pkl` | Model `.pkl` files skipped by git | Run `git add models/*.pkl -f` and push to GitHub. |
| `UnicodeEncodeError` in logs | Non-ASCII console print | Fixed in V2.0 codebase (clean UTF-8 / ASCII fallbacks active). |
| `APIKeyMissingError` | Gemini API key not configured | Add `GEMINI_API_KEY` under Streamlit Cloud **App Settings -> Secrets**. |

---

## 🔄 Step 7: Updating Future Versions Independently

Because this project is linked to `AI-Career-Intelligence-Platform-V2`, future updates are isolated:

```bash
# Push updates strictly to Version 2.0 without affecting V1
git add .
git commit -m "fix: updated feature enhancements"
git push origin-v2 main
```
 Streamlit Cloud will automatically re-deploy your Version 2.0 application in seconds!
