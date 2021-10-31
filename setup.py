import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="privacyHE",
    version="0.1.1",
    description="Framework for end to end processing on encrypted data with python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/thewires2/Privacy",
    author="Arnav Bagchi",
    author_email="arnavbagchi04@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["privacyHE"],
    include_package_data=True,
)

