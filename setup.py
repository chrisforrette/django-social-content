import os

from setuptools import setup, find_packages

import social_content


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


url = 'https://github.com/chrisforrette/django-social-content'

setup(
    name='django-social-content',
    version=social_content.__version__,
    description='Store social user accounts and their posts in a database in your Django project',
    long_description=README,
    keywords='django, social, api, content, import',
    author='Chris Forrette',
    author_email='chris@chrisforrette.com',
    url=url,
    download_url='{}/tarball/v{}'.format(url, social_content.__version__),
    license='MIT',
    packages=find_packages(),
    package_data={'README': ['README.md']},
    install_requires=[
        'pytz==2015.7',
        'python-dateutil==2.4.2',
        'django-model-utils==2.4',
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
        'Framework :: Django',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ]
)
