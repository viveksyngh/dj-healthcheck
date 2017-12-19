import os
from setuptools import setup, find_packages

# Allow setup.py to run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dj-healthcheck',
    packages=['healthcheck'],
    version='0.1',
    description='A Django App to get health status of different services used \
by a Django project',
    author='Vivek Singh',
    author_email='vivekkmr45@yahoo.in',
    install_requires=[
        'redis==2.10.6',
        'simple-salesforce==0.73.0'
    ]
)

