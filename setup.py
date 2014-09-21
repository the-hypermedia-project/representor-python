import sys, os
from setuptools import setup, find_packages
import hypermedia_resource

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(name='hypermedia_resource',
      version=hypermedia_resource.__version__,
      description='Generic interface for hypermedia messages',
      author='Stephen Mizell',
      author_email='smizell@gmail.com',
      url='https://github.com/the-hypermedia-project/hypermedia-resource-python/',
      packages=['hypermedia_resource',
                'hypermedia_resource.adapters',
                'hypermedia_resource.contrib'],
      license='MIT',
      test_suite="tests")
