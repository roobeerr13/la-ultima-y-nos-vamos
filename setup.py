from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="la_ultima_y_nos_vamos",
    version="0.1.0",
    author="[Your Name]",
    author_email="[Your Email]",
    description="Interactive voting app for streamers with polls, AI chatbot, and NFT tokens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/[Your GitHub Username]/la-ultima-y-nos-vamos",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "gradio>=3.0",
        "transformers",
        "pytest",
        "bcrypt",
        "pytest-cov",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "streamapp=src.app:main",
        ],
    },
)