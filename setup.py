from setuptools import setup

with open("README.rst") as f:
    readme = f.read()

setup(
    name="joommfutil",
    version="0.5.4.2",
    description="A JOOMMF utilities package.",
    long_description=readme,
    author="Computational Modelling Group",
    author_email="fangohr@soton.ac.uk",
    url="https://github.com/joommf/joommfutil",
    download_url="https://github.com/joommf/joommfutil/tarball/0.5.4.2",
    packages=["joommfutil",
              "joommfutil.typesystem",
              "joommfutil.tests"],
    install_requires=["numpy"],
    classifiers=["License :: OSI Approved :: BSD License",
                 "Programming Language :: Python :: 3"]
)
