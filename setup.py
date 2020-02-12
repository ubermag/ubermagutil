import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='ubermagutil',
    version='0.2.2',
    description=('Python utilities package used across '
                 'most of Ubermag packages.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://ubermag.github.io',
    author='Marijan Beg and Hans Fangohr',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['numpy',
                      'pytest'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 3 :: Only',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Topic :: Scientific/Engineering :: Physics',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English']
)
