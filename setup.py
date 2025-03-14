from setuptools import setup, find_packages
from pathlib import Path

# version
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("dplibraries", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0")

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="deploypilot",
    version=version,
    install_requires=install_requires,
    package_dir={"dplibraries": "dplibraries"},
    python_requires=">=3.6",
    packages=find_packages(where=".", exclude=["docs", "examples", "tests"]),
    author="DeployPilot",
    author_email="deploypilot@gmail.com",
    description="Deployment automation service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EdouardWP/deploypilot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 