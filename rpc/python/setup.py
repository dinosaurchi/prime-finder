import setuptools
import versioneer
import os


parent_dir = os.path.dirname(__file__)

with open(os.path.join(parent_dir, 'README.md'), 'r') as fh:
	long_description = fh.read()

with open(os.path.join(parent_dir, 'requirements.txt'), 'r') as f:
	requirements = [line for line in f.readlines() if len(line) > 0 and not 'oandapy' in line]

setuptools.setup(
	name='prime_proto',
	version=versioneer.get_version(),
	cmdclass=versioneer.get_cmdclass(),
	author='Tinh-Chi TRAN',
	author_email='tinhchi.tran@gmail.com',
	description='Protobuf-Protocols for calculating largest prime',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/dinosaurchi/stably-interview',
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