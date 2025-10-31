#!/usr/bin/env python3
"""
Clean Starter for File System MCP Server + GitHub Agent
"""
import os
import sys

def main():
    print("🚀 File System MCP Server + GitHub Agent")
    print("=" * 50)
    
    print("\n📁 Available Components:")
    print("1. File System MCP Server (fs_server.py)")
    print("2. GitHub Agent (github_agent_updated.py)")
    print("3. File System Demo (demo_fs_fixed.py)")
    print("4. Exit")
    
    try:
        choice = input("\n🎯 Choose option (1-4): ").strip()
        
        if choice == "1":
            print("\nStarting File System MCP Server...")
            os.system("python fs_server.py")
            
        elif choice == "2":
            print("\nStarting GitHub Agent...")
            os.system("python github_agent_updated.py")
            
        elif choice == "3":
            print("\nRunning File System Demo...")
            os.system("python demo_fs_fixed.py")
            
        elif choice == "4":
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
