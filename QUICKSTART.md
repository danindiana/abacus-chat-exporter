# Quick Start Guide

## 1. Activate Virtual Environment & Install Dependencies

The project comes with a pre-configured Python 3 virtual environment:

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate  # Activate the venv
```

Or use the convenience script:
```bash
source activate.sh
```

If you need to recreate the environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure Your API Key

Create a `.env` file with your credentials:

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Add your API key:
```
ABACUS_API_KEY=your-actual-api-key-here
DEPLOYMENT_ID=your-deployment-id-here  # optional, only if exporting deployments
```

## 3. Run the Export

### Export Everything (Recommended)
```bash
./export_all.sh
```

### Export Only AI Chat Sessions
```bash
export ABACUS_API_KEY="your-api-key"
python bulk_export_ai_chat.py
```

### Export Only Deployment Conversations
```bash
export ABACUS_API_KEY="your-api-key"
export DEPLOYMENT_ID="your-deployment-id"
python bulk_export_deployment_convos.py
```

## 4. Find Your Exports

- AI Chat exports: `abacus_ai_chat_exports/`
- Deployment exports: `abacus_deployment_{ID}_exports/`

Each chat will have:
- `.html` file - Human-readable, ready to open in browser
- `.json` file - Full data for archival/processing (AI Chat only)

## Need Help?

See `README.md` for full documentation and troubleshooting tips.
