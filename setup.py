import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.abspath(__file__))


def read(filename):
    fullpath = os.path.join(current_dir, filename)
    try:
        with open(fullpath) as f:
            return f.read()
    except Exception:
        return ""


setup(
    name='chaser',
    version='0.1',
    description="",
    long_description=read('README.rst'),
    packages=find_packages(),
    author='Shinya Okano',
    author_email='tokibito@gmail.com',
    url='https://github.com/tokibito/python-chaser',
    install_requires=[],
    extras_require={
        "dev": [
            "flake8",
            "pytest",
            "wheel",
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ])
