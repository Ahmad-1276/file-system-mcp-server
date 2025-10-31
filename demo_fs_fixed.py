#!/usr/bin/env python3
import os
import sys

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(__file__))

from fs_server import (
    scan_directory_tool,
    get_file_metadata_tool,
    read_text_file_tool,
    search_files_tool,
    list_directory
)

def demo_file_system():
    """Demo the file system functions"""
    print("📁 File System Demo")
    print("=" * 50)
    
    # Demo 1: List current directory
    print("\n1. 📂 Listing current directory:")
    result = list_directory(".")
    if not result.get("error"):
        print(f"   Files: {result.get('file_count', 0)}")
        print(f"   Directories: {result.get('directory_count', 0)}")
        print(f"   Path: {result.get('path', '')}")
        
        # Show some files and directories
        files = result.get('files', [])[:3]
        dirs = result.get('directories', [])[:3]
        
        if files:
            print("   Sample files:")
            for file in files:
                print(f"     - {file.get('name')} ({file.get('type')})")
        
        if dirs:
            print("   Sample directories:")
            for dir in dirs:
                print(f"     - {dir.get('name')}")
    else:
        print(f"   Error: {result.get('error')}")
    
    # Demo 2: Get metadata of this file
    print("\n2. 📄 Getting file metadata:")
    result = get_file_metadata_tool(__file__)
    if not result.get("error"):
        print(f"   Name: {result.get('name')}")
        print(f"   Size: {result.get('size')} bytes")
        print(f"   Type: {result.get('type')}")
        print(f"   Created: {result.get('created')}")
        if result.get('line_count'):
            print(f"   Lines: {result.get('line_count')}")
    else:
        print(f"   Error: {result.get('error')}")
    
    # Demo 3: Scan for Python files
    print("\n3. 🔍 Scanning for Python files:")
    result = scan_directory_tool(".", recursive=False)
    if not result.get("error"):
        files = result.get('files', [])
        python_files = [f for f in files if f.get('name', '').endswith('.py')]
        print(f"   Found {len(python_files)} Python files:")
        for file in python_files[:5]:
            print(f"   - {file.get('name')} ({file.get('size')} bytes)")
    else:
        print(f"   Error: {result.get('error')}")
    
    # Demo 4: Read this demo file
    print("\n4. 📖 Reading this demo file (first 10 lines):")
    result = read_text_file_tool(__file__, max_lines=10)
    if not result.get("error"):
        content = result.get('content', '')
        print("   Content preview:")
        lines = content.split('\n')
        for i, line in enumerate(lines[:10], 1):
            print(f"   {i:2d}: {line}")
        if len(lines) > 10:
            print(f"   ... and {len(lines) - 10} more lines")
    else:
        print(f"   Error: {result.get('error')}")
    
    # Demo 5: Search for files
    print("\n5. 🔎 Searching for files containing 'test':")
    result = search_files_tool(".", "test", recursive=False)
    if not result.get("error"):
        matches = result.get('matches', [])
        print(f"   Found {len(matches)} files matching 'test':")
        for match in matches[:3]:
            print(f"   - {match.get('name')}")
        if len(matches) > 3:
            print(f"   ... and {len(matches) - 3} more")
    else:
        print(f"   Error: {result.get('error')}")
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    demo_file_system()
