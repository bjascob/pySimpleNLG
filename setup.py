import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simplenlg',
    version='0.1.0',
    author='Brad Jascob',
    author_email='bjascob@msn.com',
    description='Python Implementation of SimpleNLG',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bjascob/pySimpleNLG',
    include_package_data=True,
    package_data={'':['default-lexicon.xml']},
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
        "Operating System :: OS Independent",
    ],
)
