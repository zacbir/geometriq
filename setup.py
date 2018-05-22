import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geometer",
    version="0.0.1",
    author="Zachery Bir",
    author_email="zbir@zacbir.net",
    description="A simple API for 2D graphics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zacbir/geometer",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

