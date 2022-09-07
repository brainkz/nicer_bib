import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nicer_bib",
    version="0.1",
    author="Rassul Bairamkulov",
    author_email="rassul.bairamkulov@epfl.ch",
    description="""A small utility for making BibTeX in your clipboard nicer.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
