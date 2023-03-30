import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pykrakenfiles",
    version="0.0.1",
    author="bontoutou",
    description="Krakenfiles upload API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['krakenfiles', 'upload'],
    url="https://github.com/bontoutou00/pykrakenfiles",
    project_urls={
        "Bug Tracker": "https://github.com/bontoutou00/pykrakenfiles/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=['requests', 'tqdm', 'requests_toolbelt']
)
