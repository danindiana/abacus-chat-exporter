# PDF Batch Processing for Abacus.AI

## Overview

The `process_pdfs.py` script automates the bulk upload and processing of PDF documents through Abacus.AI deployments. It processes each PDF with three sequential prompts to extract comprehensive insights.

## Features

- 📁 **Directory Scanning**: Browse local or remote directories for PDFs
- 🔄 **Recursive Search**: Optional subdirectory scanning
- 📤 **Batch Upload**: Automated PDF upload to Abacus.AI deployments
- 🤖 **Three-Stage Processing**:
  1. **Summarize**: Generate paper summary
  2. **Symbolic Logic**: Extract core insights as symbolic logic
  3. **C++ Examples**: Demonstrate insights with C++ code
- 📝 **Activity Logging**: JSON log of all operations
- ✅ **Confirmation**: Verify each upload/processing step

## Prerequisites

1. **Python Environment**: Use the existing venv
2. **API Key**: Abacus.AI API key set as environment variable
3. **Deployment ID**: Target deployment for processing

## Installation

Already installed! The script uses the existing virtual environment.

```bash
cd ~/programs/abacus-chat-exporter
source venv/bin/activate
```

## Usage

### Basic Usage

```bash
export ABACUS_API_KEY="your-api-key-here"
./process_pdfs.py
```

### Interactive Prompts

The script will prompt you for:

1. **Deployment ID**: The Abacus.AI deployment to use
   ```
   🎯 Enter Deployment ID: bb403b4ba
   ```

2. **Source Directory**: Path to folder containing PDFs
   ```
   📁 Enter source directory path: /home/jeb/papers
   ```

3. **Recursive Scan**: Whether to search subdirectories
   ```
   🔄 Scan subdirectories recursively? (Y/n) [default: Y]: Y
   ```

4. **Confirmation**: Review before processing
   ```
   📋 Ready to process 10 PDFs with deployment: bb403b4ba
   Proceed? (Y/n) [default: Y]: Y
   ```

## Processing Steps

For each PDF, the script:

1. **Upload**: Upload PDF to deployment
2. **Create Conversation**: Initiate deployment conversation
3. **Prompt A**: "Summarize this paper"
4. **Prompt B**: "Refactor the paper's core insights using symbolic logic"
5. **Prompt C**: "Refactor the paper's core insights using C++ code examples"
6. **Log Results**: Save to JSON activity log

## Output

### Console Output

```
================================================================================
🚀 Abacus.AI PDF Batch Processor
================================================================================

🎯 Enter Deployment ID: bb403b4ba

📁 Enter source directory path: /home/jeb/research/papers

🔄 Scan subdirectories recursively? (Y/n) [default: Y]: Y

🔍 Scanning for PDFs (recursive)...
✅ Found 15 PDF file(s)

================================================================================
📋 Ready to process 15 PDFs with deployment: bb403b4ba
================================================================================

Proceed? (Y/n) [default: Y]: Y

================================================================================
🎬 Starting batch processing...
================================================================================

[1/15] Processing: neural_networks_paper.pdf
--------------------------------------------------------------------------------
  📤 Uploading: neural_networks_paper.pdf...
  ✅ Upload successful: neural_networks_paper.pdf

  💬 Processing: neural_networks_paper.pdf
  🆔 Conversation ID: 7fb27921f
  🤖 Prompt: summarize...
  ✅ summarize complete
  🤖 Prompt: symbolic_logic...
  ✅ symbolic_logic complete
  🤖 Prompt: cpp_examples...
  ✅ cpp_examples complete

📝 Activity logged to: pdf_processing_logs/processing_activity.json
--------------------------------------------------------------------------------
```

### Activity Log

JSON file saved to `pdf_processing_logs/processing_activity.json`:

```json
{
  "processed_files": [
    {
      "timestamp": "2025-10-21T14:30:00.123456",
      "file_number": 1,
      "total_files": 15,
      "pdf_path": "/home/jeb/research/papers/neural_networks.pdf",
      "pdf_name": "neural_networks.pdf",
      "deployment_id": "bb403b4ba",
      "upload": {
        "status": "success",
        "filename": "neural_networks.pdf",
        "path": "/home/jeb/research/papers/neural_networks.pdf",
        "upload_response": "..."
      },
      "processing": {
        "conversation_id": "7fb27921f",
        "summarize": {
          "prompt": "Summarize this paper.",
          "response": "...",
          "status": "success"
        },
        "symbolic_logic": {
          "prompt": "Refactor the paper's core insights using symbolic logic.",
          "response": "...",
          "status": "success"
        },
        "cpp_examples": {
          "prompt": "Refactor the paper's core insights using C++ code examples.",
          "response": "...",
          "status": "success"
        }
      },
      "overall_status": "success"
    }
  ],
  "last_updated": "2025-10-21T14:35:00.123456"
}
```

## Finding Your Deployment ID

### Method 1: From Web UI
1. Go to Abacus.AI web interface
2. Navigate to your project
3. Find your deployment
4. Copy the deployment ID from the URL or deployment details

### Method 2: Using API Script
```bash
python find_all_deployment_conversations.py
```

## Error Handling

- **Upload Failures**: Logged and script continues with next file
- **Processing Failures**: Individual prompt failures logged, continues to next prompt
- **API Errors**: Detailed error messages in console and activity log
- **Interruption**: Ctrl+C safely exits with partial log saved

## Activity Log Location

All logs saved to: `pdf_processing_logs/processing_activity.json`

The log is **cumulative** - each run appends to the existing log file.

## Tips

1. **Small Test First**: Start with 1-2 PDFs to verify deployment works
2. **Monitor Console**: Watch for upload/processing confirmations
3. **Check Logs**: Review activity log after completion
4. **Deployment Limits**: Be aware of API rate limits
5. **Large Batches**: For 100+ PDFs, consider running in batches

## Troubleshooting

### API Key Issues
```bash
# Verify API key is set
echo $ABACUS_API_KEY

# Set if missing
export ABACUS_API_KEY="your-key"
```

### No PDFs Found
```bash
# Check directory exists
ls -la /path/to/pdfs

# Verify PDF files present
find /path/to/pdfs -name "*.pdf"
```

### Upload Failures
- Check deployment ID is correct
- Verify deployment accepts document uploads
- Check PDF file isn't corrupted

### API Method Compatibility
The script uses standard Abacus.AI SDK methods. If you encounter method errors:
1. Check SDK version: `pip show abacusai`
2. Update if needed: `pip install -U abacusai`
3. Refer to official SDK docs for correct method names

## Advanced Usage

### Custom Prompts

To modify the prompts, edit the `prompts` list in `process_with_prompts()`:

```python
prompts = [
    ("summarize", "Summarize this paper."),
    ("symbolic_logic", "Refactor the paper's core insights using symbolic logic."),
    ("cpp_examples", "Refactor the paper's core insights using C++ code examples.")
]
```

### Processing Specific Files

Instead of directory scanning, you can modify the script to process a specific list:

```python
pdf_files = [
    pathlib.Path("/path/to/paper1.pdf"),
    pathlib.Path("/path/to/paper2.pdf")
]
```

## Related Scripts

- `export_all.sh` - Export conversation history
- `find_all_deployment_conversations.py` - List deployments and conversations
- `bulk_export_all_deployment_conversations.py` - Bulk export chats

## Support

For issues or questions:
1. Check the activity log for detailed error messages
2. Verify API key and deployment ID
3. Review Abacus.AI SDK documentation
4. Check deployment conversation limits

## Example Workflow

```bash
# 1. Activate environment
cd ~/programs/abacus-chat-exporter
source venv/bin/activate

# 2. Set API key
export ABACUS_API_KEY="your-key"

# 3. Find your deployment ID
python find_all_deployment_conversations.py

# 4. Run processor
./process_pdfs.py
# Enter deployment ID: bb403b4ba
# Enter directory: /home/jeb/papers
# Recursive? Y
# Confirm? Y

# 5. Review results
cat pdf_processing_logs/processing_activity.json | jq
```
