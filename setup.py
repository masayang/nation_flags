from setuptools import setup

setup(
    name='nation_flags',
    version='1.0',
    long_description=__doc__,
    packages=['nation_flags', 'tests'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['coverage', 'lxml', 'mock', 'nose', 'nose-watch', 'python-dotenv', 'requests']
)