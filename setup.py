from setuptools import setup, find_packages
import hypermedia_resource

setup(name='HypermediaResource',
    version=hypermedia_resource.__version__,
    description='Generic interface for hypermedia messages',
    author='Stephen Mizell',
    author_email='smizell@gmail.com',
    url='https://github.com/the-hypermedia-project/hypermedia-resource-python/',
    packages=['hypermedia_resource'],
    license='MIT',
    test_suite="tests")
