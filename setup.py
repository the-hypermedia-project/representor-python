from setuptools import setup, find_packages
import hypermedia_resource

setup(name='hypermedia_resource',
    version=hypermedia_resource.__version__,
    description='Generic interface for hypermedia messages',
    author='Stephen Mizell',
    author_email='smizell@gmail.com',
    url='https://github.com/the-hypermedia-project/hypermedia-resource-python/',
    download_url='https://github.com/the-hypermedia-project/hypermedia-resource-python/archive/0.1.1.tar.gz',
    packages=['hypermedia_resource'],
    license='MIT',
    test_suite="tests")
