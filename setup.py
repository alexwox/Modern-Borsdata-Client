from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="borsdata-client",
    version="0.1.0",
    author="alexwox",
    author_email="aw@woxst.ai",
    description="A modern third party Python client for the Borsdata API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexwox/Modern-Borsdata-Client",
    project_urls={
        "Bug Tracker": "https://github.com/alexwox/Modern-Borsdata-Client/issues",
        "Documentation": "https://github.com/alexwox/Modern-Borsdata-Client#readme",
        "Source Code": "https://github.com/alexwox/Modern-Borsdata-Client",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="borsdata, finance, api, stocks, market data",
) 