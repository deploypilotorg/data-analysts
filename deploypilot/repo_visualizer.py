from deploypilot.github_client import GitHubClient

class RepoVisualizer:
    def __init__(self):
        self.github_client = GitHubClient()

    def generate_repo_diagram(self, repo_name):
        """Generate a Mermaid.js diagram of the repository structure."""
        structure = self.github_client.get_repo_structure(repo_name)
        if "error" in structure:
            return structure["error"]
        
        diagram = "graph TD;\n"
        nodes = set()
        links = set()
        
        for path in structure:
            parts = path.split("/")
            for i in range(len(parts)):
                if i == 0:
                    parent = "root"
                else:
                    parent = "/".join(parts[:i])
                child = "/".join(parts[:i+1])
                
                nodes.add(child)
                links.add(f"    {parent} --> {child}")
        
        diagram += "\n".join(links)
        return diagram