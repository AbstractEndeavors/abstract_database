from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='abstract_database',
    version='0.0.2.188',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description="Lazy, environment-driven PostgreSQL connection management with multi-database support and table/query helpers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AbstractEndeavors/abstract_database",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['pillow' ,
                      'abstract_apis' ,
                      'abstract_gui' ,
                      'abstract_math' ,
                      'abstract_security',
                      'asyncpg',
                      'abstract_utilities' ,
                      'numpy' ,
                      'pandas' ,
                      'psycopg[binary]' ,
                      'sqlalchemy',
                      ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # Add this line to include wheel format in your distribution
    setup_requires=['wheel'],
)

 
