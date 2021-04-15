from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as file:
    readme = file.read()

setup(
    name='pgbackup',
    version='0.1.0',
    description='Database backups locally or to AWS S3.',
    long_description=readme,
    author='Dennis Lee',
    author_email='dennislwm@gmail.com',
    install_requires=['boto3'],
    entry_points={
        'console_scripts': [
            'pgbackup=pgbackup.cli:main',
        ]
    },
    packages=find_packages('src'),
    package_dir={'': 'src'}
)
