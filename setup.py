from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='proxychecker',
    version='0.1.0',
    author='Amani Toama',
    author_email='amanitoama570@gmail.com',
    description='A tool to check the status and speed of proxy servers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AmaniToamaWebDevelp1/proxychecker.git',
    packages=find_packages(),
    py_modules=['proxy_checker'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
       'requests',  # Dependency
        'colorama',  
    ],
    entry_points={
        'console_scripts': [
            'proxy_checker=proxy_checker:main',
        ],
       keywords='proxy checker',
    },
)
