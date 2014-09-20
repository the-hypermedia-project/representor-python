from setuptools import setup, find_packages
import hypermedia_resource

download_url = 'https://github.com/the-hypermedia-project/hypermedia-resource-python/archive/'+hypermedia_resource.__version__+'.tar.gz'

setup(name='hypermedia_resource',
    version=hypermedia_resource.__version__,
    description='Generic interface for hypermedia messages',
    author='Stephen Mizell',
    author_email='smizell@gmail.com',
    url='https://github.com/the-hypermedia-project/hypermedia-resource-python/',
    download_url=download_url,
    packages=['hypermedia_resource'],
    license='MIT',
    test_suite="tests")
