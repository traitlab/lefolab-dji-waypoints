import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lefolab-drone-src",
    version="0.7.3",
    author="Vincent Le Falher",
    author_email="vincent.lefalher@umontreal.ca",
    description="LEFO LAB DJI KMZ Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincelf-IVADO/lefolab-drone-src",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.10',
    install_requires=[
        "pydantic", "pyyaml", "shapely",
        "geopandas", "rasterio", "pyproj", "networkx"
    ],
    entry_points={
        'console_scripts': [
            'lefolab-drone=src.main:main',
        ],
    },
    license="GNU General Public License v3"
)
