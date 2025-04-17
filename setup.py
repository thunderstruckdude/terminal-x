from setuptools import setup, find_packages

setup(
    name="terminalx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "anthropic",  # For Claude API
        "google-generativeai",  # For Gemini API
        "rich",  # For terminal styling
        "pyyaml",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "terminal=terminalx.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Natural Language Terminal Command Assistant",
)