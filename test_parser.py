"""
Simple test script to verify the resume parser works with sample files.
"""

import os
import sys
from app.parser import process_resume_file

def test_parser():
    """Test the parser with sample files."""
    print("Resume Parser Test")
    print("-----------------")
    
    # Test directory with sample files
    test_dir = "test_files"
    
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"Created directory {test_dir}")
        print(f"Please add sample resume files (.pdf, .docx, .doc) to {test_dir} and run again.")
        return
    
    files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.pdf', '.docx', '.doc'))]
    
    if not files:
        print(f"No sample files found in {test_dir}")
        print(f"Please add sample resume files (.pdf, .docx, .doc) to {test_dir} and run again.")
        return
    
    for filename in files:
        file_path = os.path.join(test_dir, filename)
        print(f"\nTesting with file: {filename}")
        
        try:
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
                
            result = process_resume_file(file_bytes, filename)
            
            if result["success"]:
                print(f"Success! Extracted {result.get('word_count', 0)} words.")
                # Print first 100 characters as preview
                preview = result["text"][:100].replace('\n', ' ').strip()
                print(f"Preview: {preview}...")
            else:
                print(f"Failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"Error processing file: {e}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    test_parser() 