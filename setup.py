from setuptools import setup, find_packages

setup(
    name="indicador_iqt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["numpy", "pandas", "geopandas", "folium"],
    author="Yago Henrique Veloso Maia",
    author_email="yagohenriquev123@gmail.com",
    description="A brief description of your library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YagoMaia/indicador_iqt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
