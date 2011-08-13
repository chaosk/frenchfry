import os
from setuptools import setup, find_packages

def read_file(filename):
	"""Read a file into a string"""
	path = os.path.abspath(os.path.dirname(__file__))
	filepath = os.path.join(path, filename)
	try:
		return open(filepath).read()
	except IOError:
		return ''

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('frenchfry').__doc__.splitlines()).strip()

setup(
	name = "frenchfry",
	version = __import__('frenchfry').get_version().replace(' ', '-'),
	url = 'https://github.com/chaosk/frenchfry',
	author = 'Krzysztof Socha',
	author_email = 'ksocha+frenchfry@ksocha.com',
	description = DESC,
	packages = find_packages(),
	include_package_data = True,
	install_requires=read_file('requirements.txt'),
	classifiers = [
		'License :: OSI Approved :: BSD License',
		'Framework :: Django',
	],
)
