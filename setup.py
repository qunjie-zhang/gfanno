# -*- coding:utf-8 -*-
from setuptools import setup
from setuptools import find_packages
import os

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='gfanno',
    version='1.0',
    description='Gene Family Annotation',
    long_description=readme(),  # 长文描述
    long_description_content_type='text/markdown',  # 长文描述的文本格式
    author=['wangzt','duliuxu'],
    author_email='interestingcn01@gmail.com',
    url='https://github.com/qunjie-zhang/gfanno',
    keywords=["gene family",'bioinformatics','pipline'],
    packages=find_packages(),
    python_requires='>=3.5',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
    entry_points={
        'console_scripts': [
            'gfanno = gfanno.__main__:main',
        ]
    },
    include_package_data = True
)