
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# get __version__
exec(open('src/scing/version.py').read())

setuptools.setup(
    name="scing",
    version=__version__,
    author="Jaeyoung Chun",
    author_email="chunj@mskcc.org",
    description="Single-Cell pIpeliNe Garden",    
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hisplan/scing",    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    # packages=setuptools.find_packages(),    
    packages=[
        "scing",
        "docker"
    ],
    package_dir={"": "src"},
    scripts=[
        "src/bin/scing"
    ],
    install_requires=[
        "pyyaml==5.4.1",
        "requests==2.24.0",
        "tqdm==4.62.0"
    ],
    extras_require={
        "dev": [
            "pytest",
            "black==21.7b0"
        ]
    }
)
