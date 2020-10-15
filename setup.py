import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SjTree-LBAI-InfoLab", # Replace with your own username
    version="0.0.1",
    author="LBAI-InfoLab",
    author_email="lbai.bioinfo@gmail.com",
    description="pSS cluster predictor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LBAI-InfoLab/SjTree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
