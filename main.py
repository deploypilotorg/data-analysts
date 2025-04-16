from dplibraries.generators.deployment_generator import DeploymentGenerator
from typing import Optional, Dict, Any
import re
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint

console = Console()

def is_valid_github_url(url: str) -> bool:
    """Validate if the input is a valid GitHub repository URL."""
    pattern = r'^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?$'
    return bool(re.match(pattern, url))

def is_unspecified_input(text: str) -> bool:
    """
    Returns True if the user's input is a vague/unspecified way of saying "I don't know".
    """
    vague_inputs = [
        "", "?", "idk", "i don't know", "whatever", "not sure",
        "you decide", "recommend one", "anything", "no idea", "you choose", "i'm not sure",
        "i don't care", "unsure", "don't know", "no preference", "just pick one",
        "i don't mind", "choose for me", "help me decide", "pick one for me",
        "let's go with anything", "i'm open to suggestions", "i don't have a preference",
        "i'm flexible", "just suggest something", "i'm indifferent", "i have no clue",
    ]
    return text.strip().lower() in vague_inputs

def get_repo_info(url: str) -> Dict[str, str]:
    """Extract repository information from GitHub URL."""
    parts = url.rstrip("/").split("/")[-2:]
    return {
        "owner": parts[0],
        "name": parts[1],
        "full_name": "/".join(parts)
    }

def display_welcome() -> None:
    """Display welcome message and instructions."""
    console.print(Panel.fit(
        "[bold blue]🚀 DeployPilot - Intelligent Deployment Advisor[/bold blue]\n\n"
        "This tool will help you deploy your project to the most suitable platform.\n"
        "We'll analyze your repository and recommend the best deployment solution.",
        title="Welcome",
        border_style="blue"
    ))

def get_user_input() -> tuple[str, Optional[str]]:
    """Get and validate user input."""
    while True:
        repo_url = Prompt.ask(
            "[bold]Enter GitHub repository URL[/bold]",
            default="https://github.com/username/repository"
        )
        
        if is_valid_github_url(repo_url):
            break
        console.print("[red]❌ Invalid GitHub URL format. Please try again.[/red]")
    
    deployment_type = Prompt.ask(
        "[bold]Enter target deployment platform[/bold]",
        choices=["AWS", "Firebase", "Vercel", "Google Cloud", "Heroku", "Netlify", "DigitalOcean"],
        default=""
    )
    
    return repo_url, deployment_type

def main() -> None:
    try:
        display_welcome()
        repo_url, deployment_type = get_user_input()
        repo_info = get_repo_info(repo_url)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing repository...", total=None)
            
            generator = DeploymentGenerator()
            
            if is_unspecified_input(deployment_type):
                console.print("\n[bold yellow]🤔 No deployment target specified. Analyzing project structure...[/bold yellow]")
                structure = generator._get_project_structure(repo_info["full_name"])
                recommended = generator.recommend_deployment_target(
                    repo_name=repo_info["name"],
                    project_structure=structure
                )
                
                console.print(f"\n[bold green]✅ Recommendation:[/bold green] {recommended}")
                if Confirm.ask("Proceed with this recommendation?"):
                    deployment_type = recommended
                else:
                    deployment_type = Prompt.ask(
                        "Enter your preferred deployment platform",
                        choices=["AWS", "Firebase", "Vercel", "Google Cloud", "Heroku", "Netlify", "DigitalOcean"]
                    )
            
            progress.update(task, description="Generating deployment files...")
            result = generator.generate_files(
                deployment_type=deployment_type,
                repo_name=repo_info["name"],
                repo_url=repo_url
            )
            
            console.print("\n[bold green]📦 Generated Deployment Files:[/bold green]")
            for filename, content in result.items():
                console.print(Panel(
                    f"[bold]{filename}[/bold]\n{content[:500]}...",
                    title="File Preview",
                    border_style="green"
                ))
                
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Operation cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
