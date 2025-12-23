from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Reads a requirements file and returns a list of dependencies."""
    requirement_lst = []
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        return []  # Return an empty list if the file is not found
    return requirement_lst

setup(
    name="NetworkSecurityProject",
    version="0.0.1",
    author="Shounak Sushanta Dasgupta",
    author_email="shounaksushantadasgupta1991@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)