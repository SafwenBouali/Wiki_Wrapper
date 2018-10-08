import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikiwrap",
    version="0.3",
    author="Safwen Bouali",
    author_email="safwen.bouali@outlook.com",
    description="Few more functions that can wrap and handle the \"Wikipedia\" package in python, made into one package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SafwenBouali/wikiwrap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)