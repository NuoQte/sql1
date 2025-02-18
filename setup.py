from setuptools import setup, find_packages

setup(
    name='mrdb',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    description="An asynchronous Python ORM that supports MySQL, SQLite, and PostgreSQL with robust performance and easy-to-use interface.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='NuoQTe',
    author_email='nuoqte@gmail.com',
    url='https://github.com/NuoQte/mrdb',
)