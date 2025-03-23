#
from dplibraries.generators.deployment_generator import DeploymentGenerator

def is_unspecified_input(text: str) -> bool:
    """
    Returns True if the user's input is a vague/unspecified way of saying "I don't know".
    """
    vague_inputs = [
        "", "?", "idk", "i don't know", "whatever", "not sure",
        "you decide", "recommend one", "anything", "no idea"
    ]
    return text.strip().lower() in vague_inputs

if __name__ == "__main__":
    print("🚀 DeployPilot - Deployment Advisor\n")
    repo_url = input("Enter a GitHub repository URL (e.g., https://github.com/user/project): ")
    deployment_type = input("Enter target deployment platform (AWS, Firebase, Vercel, Google Cloud) or leave blank if unsure: ")

    try:
        generator = DeploymentGenerator()

        # Auto-recommend deployment platform if user is unsure
        if is_unspecified_input(deployment_type):
            print("\n🤔 You didn't specify a deployment target. We'll help with that...\n")
            parts = repo_url.rstrip("/").split("/")[-2:]
            full_repo_name = "/".join(parts)
            structure = generator._get_project_structure(full_repo_name)
            recommended = generator.recommend_deployment_target(repo_name=parts[1], project_structure=structure)
            
            print(f"✅ Based on the project, we recommend: **{recommended}**")
            confirm = input("Do you want to proceed with this recommendation? (y/n): ").strip().lower()
            if confirm != "y":
                deployment_type = input("Okay, please enter your preferred deployment platform: ")
            else:
                deployment_type = recommended

        result = generator.generate_files(
            deployment_type=deployment_type,
            repo_name=repo_url.split("/")[-1],
            repo_url=repo_url
        )

        print("\n📦 Recommended Deployment Files:")
        for filename, content in result.items():
            print(f"\n🔹 {filename}:\n{content[:500]}...")  # Truncate long files for readability

    except Exception as e:
        print(f"❌ Error: {str(e)}")
