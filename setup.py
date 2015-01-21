import sys, os
from setuptools import setup, find_packages
import representor

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(name='representor',
      version=representor.__version__,
      description='Generic interface for hypermedia messages',
      author='Stephen Mizell',
      author_email='smizell@gmail.com',
      url='https://github.com/the-hypermedia-project/representor-python/',
      packages=['representor',
                'representor.adapters',
                'representor.contrib'],
      license='MIT',
      test_suite="tests")
