from setuptools import setup, find_packages

import social_content


url = 'https://github.com/chrisforrette/django-social-content'

setup(
    name='django-social-content',
    version=social_content.__version__,
    description='Simple Python API client for Plaid',
    long_description='',
    keywords='django, social, api, content, import',
    author='Chris Forrette',
    author_email='chris@chrisforrette.com',
    url=url,
    download_url='{}/tarball/v{}'.format(url, social_content.__version__),
    license='MIT',
    packages=find_packages(exclude='tests'),
    package_data={'README': ['README.md']},
    install_requires=[
        'pytz==2015.7',
        'facebook-sdk==0.4.0',
        'python-instagram==1.3.2',
        'python-twitter==2.2'
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ]
)
