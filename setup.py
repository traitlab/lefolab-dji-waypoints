import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lefolab-drone-src",
    version="0.6.6",
    py_modules=['lefolab_drone_src'],
    author="Vincent Le Falher",
    author_email="vincent.lefalher@umontreal.ca",
    description="LEFO LAB DJI KMZ Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincelf-IVADO/lefolab-drone-src",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GENERAL PUBLIC LICENSE v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.10',
    install_requires=["pydantic", "pyyaml", "shapely",
                      "geopandas", "rasterio", "pyproj", "networkx"],
    license="GNU GENERAL PUBLIC LICENSE v3"
)
