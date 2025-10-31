#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

try:
    from langchain_groq import ChatGroq
    from github import Github, Auth
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages:")
    print("pip install langchain-groq PyGithub python-dotenv")
    exit(1)

# Initialize Groq LLM with current model
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        exit(1)
    
    # Updated model - using current available models
    groq_llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.1-8b-instant"  # Current working model
        # Alternative models you can try:
        # "mixtral-8x7b-32768" - if available
        # "llama-3.1-70b-versatile"
        # "gemma2-9b-it"
    )
    print("✅ Groq LLM initialized successfully with model: llama-3.1-8b-instant")
except Exception as e:
    print(f"❌ Groq initialization failed: {e}")
    print("Trying alternative model...")
    try:
        groq_llm = ChatGroq(
            groq_api_key=groq_api_key,
            model="mixtral-8x7b-32768"
        )
        print("✅ Groq LLM initialized with fallback model")
    except Exception as e2:
        print(f"❌ All Groq models failed: {e2}")
        exit(1)

# Initialize GitHub API with modern authentication
try:
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN not found in .env file")
        exit(1)
    
    # Use modern authentication
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    
    # Test the connection
    user = g.get_user()
    print(f"✅ GitHub API connected successfully as {user.login}")
    
    # Test repository access
    repos = user.get_repos().get_page(0)
    print(f"✅ Found {len(repos)} repositories")
    
except Exception as e:
    print(f"❌ GitHub API initialization failed: {e}")
    exit(1)

def handle_user_command(command: str):
    """Interpret user command using Groq and perform GitHub actions."""
    print(f"🔍 Processing command: {command}")
    
    # Get interpretation from Groq
    try:
        interpretation = groq_llm.invoke(
            f"Interpret this GitHub instruction and describe what action to take: {command}"
        )
        print(f"🧠 Groq interpretation:\n{interpretation.content}\n")
    except Exception as e:
        print(f"❌ Groq interpretation failed: {e}")
        print("⚠️ Continuing with direct GitHub commands (AI interpretation skipped)")
        # Continue without AI interpretation

    # Execute GitHub commands
    try:
        if "create repo" in command.lower() or "create repository" in command.lower():
            # Extract repo name from command
            if "create repo" in command.lower():
                name_part = command.lower().split("create repo")[-1].strip()
            else:
                name_part = command.lower().split("create repository")[-1].strip()
            
            # Clean up the name
            repo_name = name_part.replace(" ", "-").replace("_", "-")
            if not repo_name:
                return "❌ Please specify a repository name. Example: 'create repo my-new-project'"
            
            print(f"🔄 Creating repository: {repo_name}")
            user = g.get_user()
            repo = user.create_repo(
                name=repo_name,
                description=f"Repository created via GitHub Agent: {repo_name}",
                auto_init=True  # Initialize with README
            )
            return f"✅ Successfully created repository: {repo.html_url}"

        elif "list repos" in command.lower() or "list repositories" in command.lower():
            user = g.get_user()
            repos = list(user.get_repos())[:10]  # Show first 10 repos
            if repos:
                result = "📚 Your repositories:\n"
                for repo in repos:
                    result += f"- {repo.name} ({repo.stargazers_count} ⭐) - {repo.html_url}\n"
                return result
            else:
                return "📚 You don't have any repositories yet."

        elif "list issues" in command.lower():
            # Extract repo name
            if "for" in command.lower():
                repo_name = command.lower().split("for")[-1].strip()
            else:
                return "❌ Please specify which repository. Example: 'list issues for username/repo-name'"
            
            try:
                if "/" in repo_name:
                    # Full repo path like username/repo-name
                    repo = g.get_repo(repo_name)
                else:
                    # Just repo name, assume user's repo
                    user = g.get_user()
                    repo = user.get_repo(repo_name)
                
                issues = list(repo.get_issues(state="open"))
                if issues:
                    result = f"📋 Open issues in {repo_name}:\n"
                    for issue in issues[:10]:  # Show first 10 issues
                        result += f"- #{issue.number}: {issue.title}\n"
                    if len(issues) > 10:
                        result += f"... and {len(issues) - 10} more issues"
                    return result
                else:
                    return f"✅ No open issues found in {repo_name}"
            except Exception as e:
                return f"❌ Error accessing repository {repo_name}: {e}"

        else:
            return "🤔 Command not recognized. Available commands:\n- 'create repo <name>'\n- 'list repos'\n- 'list issues for <repo-name>'"
            
    except Exception as e:
        return f"❌ Error executing GitHub command: {e}"

if __name__ == "__main__":
    print("🚀 GitHub Agent (Updated Models) starting...")
    print("Available commands:")
    print("- 'create repo <name>' - Create a new repository")
    print("- 'list repos' - List your repositories")
    print("- 'list issues for <repo>' - List issues in a repository")
    print("- 'exit' - Quit the agent")
    print()
    
    while True:
        try:
            cmd = input("💬 GitHub Command > ").strip()
            if cmd.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            elif cmd:
                result = handle_user_command(cmd)
                print(f"📝 Result: {result}\n")
            else:
                print("⚠️ Please enter a command\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}\n")
