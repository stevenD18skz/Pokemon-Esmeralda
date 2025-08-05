from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pokemon-esmeralda",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    description="Un juego de Pokémon desarrollado en Python con interfaz de consola",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/Pokemon-Esmeralda",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pokemon-esmeralda=Pokemon Esmeralda - consola.Main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.db", "*.txt", "*.jpg", "*.png"],
    },
)