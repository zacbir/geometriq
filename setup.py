import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geometriq",
    version="0.2dev",
    author="Zachery Bir",
    author_email="zbir@zacbir.net",
    description="A simple API for 2D graphics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zacbir/geometriq",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'click >= 6.0',
        'opensimplex >= 0.2',
        'pyobjc;platform_system=="Darwin"',
    ],
    entry_points='''
        [console_scripts]
        geometriq=geometriq_cli:geometriq_cli
    ''',    
)