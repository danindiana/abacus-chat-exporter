# Troubleshooting Segmentation Faults

If you encounter a segmentation fault (exit code 139) when running the export scripts, this is typically caused by compatibility issues between Python 3.13 and certain C-extension libraries like numpy/pandas.

## Quick Fixes

### Option 1: Recreate venv with Python 3.11 or 3.12

```bash
cd ~/programs/abacus-chat-exporter

# Remove existing venv
rm -rf venv

# Create new venv with older Python (if available)
python3.11 -m venv venv  # or python3.12
source venv/bin/activate
pip install -r requirements.txt
```

### Option 2: Force reinstall numpy/pandas

```bash
source venv/bin/activate
pip install --upgrade --force-reinstall numpy pandas
```

### Option 3: Use the cURL alternative

The project includes a shell-based alternative that doesn't use Python:

```bash
./export_with_curl.sh
```

This requires `jq` to be installed:
```bash
sudo apt install jq  # Debian/Ubuntu
sudo yum install jq  # RHEL/CentOS
```

### Option 4: Run with debugging

To see exactly where the segfault occurs:

```bash
source venv/bin/activate
python -X dev bulk_export_ai_chat.py
```

Or use the test script:

```bash
export ABACUS_API_KEY="your-key"
python test_api.py
```

## Known Issue

Python 3.13 is very new (released October 2024) and some packages may not have fully compatible wheels yet. The abacusai package depends on pandas/numpy which have C extensions that may not be stable on Python 3.13 for all systems.

### Recommended Solution

Use Python 3.11 or 3.12 instead:

```bash
# Check available Python versions
ls /usr/bin/python3*

# Use an older version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./export_all.sh
```
