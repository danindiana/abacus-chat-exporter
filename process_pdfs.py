#!/usr/bin/env python3
"""
Abacus.AI PDF Batch Processor

Uploads PDFs from a directory to Abacus.AI and processes them with:
1. Summarize the paper
2. Refactor core insights using symbolic logic
3. Refactor core insights using C++ code examples

Usage:
    export ABACUS_API_KEY="your-key"
    python process_pdfs.py
"""

import os
import sys
import json
import pathlib
from datetime import datetime
from typing import List, Dict, Any
from abacusai import ApiClient


def get_user_input() -> tuple[pathlib.Path, bool]:
    """Prompt user for source directory and recursion option"""
    while True:
        dir_path = input("\n📁 Enter source directory path: ").strip()
        source_dir = pathlib.Path(dir_path).expanduser()
        
        if source_dir.exists() and source_dir.is_dir():
            break
        print(f"❌ Directory not found: {source_dir}")
    
    recursion_input = input("\n🔄 Scan subdirectories recursively? (Y/n) [default: Y]: ").strip().lower()
    recursive = recursion_input != 'n'
    
    return source_dir, recursive


def find_pdfs(source_dir: pathlib.Path, recursive: bool) -> List[pathlib.Path]:
    """Find all PDF files in the directory"""
    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdfs = sorted(source_dir.glob(pattern))
    return [p for p in pdfs if p.is_file()]


def sanitize_filename(name: str, max_len: int = 100) -> str:
    """Sanitize a string for use in filenames"""
    return name.replace("/", "_").replace(" ", "_").replace(":", "-").replace("(", "").replace(")", "")[:max_len]


def upload_document(client: ApiClient, deployment_id: str, pdf_path: pathlib.Path) -> Dict[str, Any]:
    """
    Upload a document to Abacus.AI deployment
    
    Returns dict with upload info or None if failed
    """
    try:
        print(f"  📤 Uploading: {pdf_path.name}...")
        
        # Upload document to deployment
        with open(pdf_path, 'rb') as f:
            # Note: Actual API method may vary - this is a typical pattern
            # You may need to adjust based on actual Abacus.AI SDK documentation
            upload_response = client.upload_document(
                deployment_id=deployment_id,
                file=f,
                filename=pdf_path.name
            )
        
        print(f"  ✅ Upload successful: {pdf_path.name}")
        return {
            'status': 'success',
            'filename': pdf_path.name,
            'path': str(pdf_path),
            'upload_response': str(upload_response)
        }
        
    except Exception as e:
        print(f"  ❌ Upload failed: {e}")
        return {
            'status': 'failed',
            'filename': pdf_path.name,
            'path': str(pdf_path),
            'error': str(e)
        }


def process_with_prompts(client: ApiClient, deployment_id: str, pdf_name: str, 
                        deployment_conversation_id: str = None) -> Dict[str, Any]:
    """
    Process the uploaded PDF with three prompts in sequence
    
    Returns dict with all responses
    """
    prompts = [
        ("summarize", "Summarize this paper."),
        ("symbolic_logic", "Refactor the paper's core insights using symbolic logic."),
        ("cpp_examples", "Refactor the paper's core insights using C++ code examples.")
    ]
    
    results = {}
    
    try:
        # Create or use existing conversation
        if not deployment_conversation_id:
            conversation = client.create_deployment_conversation(deployment_id=deployment_id)
            deployment_conversation_id = conversation.deployment_conversation_id
            results['conversation_id'] = deployment_conversation_id
        
        print(f"\n  💬 Processing: {pdf_name}")
        print(f"  🆔 Conversation ID: {deployment_conversation_id}")
        
        for prompt_key, prompt_text in prompts:
            print(f"  🤖 Prompt: {prompt_key}...")
            
            try:
                # Send message to deployment conversation
                response = client.create_deployment_conversation_message(
                    deployment_conversation_id=deployment_conversation_id,
                    message=prompt_text
                )
                
                # Get the response text
                response_text = response.response if hasattr(response, 'response') else str(response)
                
                results[prompt_key] = {
                    'prompt': prompt_text,
                    'response': response_text,
                    'status': 'success'
                }
                
                print(f"  ✅ {prompt_key} complete")
                
            except Exception as e:
                print(f"  ❌ {prompt_key} failed: {e}")
                results[prompt_key] = {
                    'prompt': prompt_text,
                    'error': str(e),
                    'status': 'failed'
                }
        
        return results
        
    except Exception as e:
        print(f"  ❌ Processing failed: {e}")
        return {
            'error': str(e),
            'status': 'failed'
        }


def save_activity_log(log_data: Dict[str, Any], output_dir: pathlib.Path):
    """Save activity log as JSON"""
    log_file = output_dir / "processing_activity.json"
    
    # Load existing log if it exists
    if log_file.exists():
        with open(log_file, 'r') as f:
            existing_data = json.load(f)
            if 'processed_files' not in existing_data:
                existing_data['processed_files'] = []
    else:
        existing_data = {'processed_files': []}
    
    # Append new entry
    existing_data['processed_files'].append(log_data)
    existing_data['last_updated'] = datetime.now().isoformat()
    
    # Save
    with open(log_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    
    print(f"\n📝 Activity logged to: {log_file}")


def main():
    print("=" * 80)
    print("🚀 Abacus.AI PDF Batch Processor")
    print("=" * 80)
    
    # Check for API key
    API_KEY = os.environ.get("ABACUS_API_KEY")
    if not API_KEY:
        print("\n❌ Error: ABACUS_API_KEY environment variable not set")
        print("   Set it with: export ABACUS_API_KEY='your-key'")
        sys.exit(1)
    
    # Get deployment ID
    deployment_id = input("\n🎯 Enter Deployment ID: ").strip()
    if not deployment_id:
        print("❌ Deployment ID is required")
        sys.exit(1)
    
    # Initialize client
    client = ApiClient(API_KEY)
    
    # Get user input
    source_dir, recursive = get_user_input()
    
    # Find PDFs
    print(f"\n🔍 Scanning for PDFs {'(recursive)' if recursive else ''}...")
    pdf_files = find_pdfs(source_dir, recursive)
    
    if not pdf_files:
        print(f"❌ No PDF files found in {source_dir}")
        sys.exit(0)
    
    print(f"✅ Found {len(pdf_files)} PDF file(s)")
    
    # Create output directory for logs
    output_dir = pathlib.Path("pdf_processing_logs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Confirm before processing
    print(f"\n{'='*80}")
    print(f"📋 Ready to process {len(pdf_files)} PDFs with deployment: {deployment_id}")
    print(f"{'='*80}")
    confirm = input("\nProceed? (Y/n) [default: Y]: ").strip().lower()
    if confirm == 'n':
        print("❌ Cancelled by user")
        sys.exit(0)
    
    # Process each PDF
    print("\n" + "=" * 80)
    print("🎬 Starting batch processing...")
    print("=" * 80)
    
    successful = 0
    failed = 0
    
    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_path.name}")
        print("-" * 80)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'file_number': idx,
            'total_files': len(pdf_files),
            'pdf_path': str(pdf_path),
            'pdf_name': pdf_path.name,
            'deployment_id': deployment_id
        }
        
        # Upload
        upload_result = upload_document(client, deployment_id, pdf_path)
        log_entry['upload'] = upload_result
        
        if upload_result['status'] == 'success':
            # Process with prompts
            processing_result = process_with_prompts(
                client, 
                deployment_id, 
                pdf_path.name
            )
            log_entry['processing'] = processing_result
            
            if processing_result.get('status') != 'failed':
                successful += 1
                log_entry['overall_status'] = 'success'
            else:
                failed += 1
                log_entry['overall_status'] = 'failed'
        else:
            failed += 1
            log_entry['overall_status'] = 'upload_failed'
        
        # Save log after each file
        save_activity_log(log_entry, output_dir)
        
        print("-" * 80)
    
    # Final summary
    print("\n" + "=" * 80)
    print("📊 BATCH PROCESSING COMPLETE")
    print("=" * 80)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total: {len(pdf_files)}")
    print(f"📝 Activity log: {output_dir / 'processing_activity.json'}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
