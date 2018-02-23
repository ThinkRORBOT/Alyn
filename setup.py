""" Setup script for installing Alyn """

from setuptools import setup

setup(
    name="alyn3",
    version="0.1.3",
    author="Kakul Chandra",
    description="Fix skew in images",
    author_email="kakulchandra911@gmail.com",
    url='https://github.com/THINKRORBOT/Alyn.git',
    download_url='https://github.com',
    keywords=['image-processing', 'image-deskew', 'deskew', 'rotate', 'text'],
    packages=['alyn3'],
    classifiers=[],
    license='MIT',
    install_requires=['numpy', 'scikit-image', 'scipy', 'matplotlib'])
