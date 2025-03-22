from dplibraries.generators.deployment_generator import DeploymentGenerator

if __name__ == "__main__":
    print("🚀 DeployPilot - Deployment Advisor\n")
    repo_url = input("Enter a GitHub repository URL (e.g., https://github.com/user/project): ")
    deployment_type = input("Enter target deployment platform (AWS, Firebase, Vercel, Google Cloud): ")

    try:
        generator = DeploymentGenerator()
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
