import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matchgrowth",
    version="0.0.1",
    author="Stefan Corneliu Petrea",
    author_email="stefan@garage-coding.com",
    description="Tool for estimating growth rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.garage-coding.com/",
    packages=setuptools.find_packages(),
    scripts=["match-growth.py"],
    install_requires=[
          'numpy>=1.19.4',
          'scipy>=1.5.4',
          'matplotlib>=3.3.3',
          'sympy>=1.7.1',
    ],
    extras_require={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
