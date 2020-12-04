import setuptools
import versioneer


with open('README.md', 'r') as fh:
	long_description = fh.read()

with open('requirements.txt', 'r') as f:
	requirements = [line for line in f.readlines() if len(line) > 0 and not 'oandapy' in line]

setuptools.setup(
	name='prime_finder_client',
	version=versioneer.get_version(),
	cmdclass=versioneer.get_cmdclass(),
	author='Tinh-Chi TRAN',
	author_email='tinhchi.tran@gmail.com',
	description='REST-API Serivce for prime finder',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/dinosaurchi/stably-interview/services/prime_finder_client',
	packages=setuptools.find_packages(exclude=['docs', 'testcases']),
	install_requires=requirements,
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6,<3.8',
	include_package_data=True,
	zip_safe=True
)