import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cellopype',
    author='Peter Kleynjan',
    author_email='peter.kleynjan@quantis.nl',
    description='Reactive dataflow pipelines for DataFrames (and other objects/variables)',
    keywords='rx, pandas, dataframe, dataflow, cell, pipeline',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kleynjan/cellopype',
    project_urls={
        'Documentation': url, 
        'Bug Reports': url + '/issues',
        'Source Code': url,
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # install_requires=['Pillow'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
)
