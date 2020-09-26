from setuptools import setup

setup(
    name="api_test",
    version="0.1.0",
    description="Blueprint for postgres with fastapi.",
    url="https://github.com/thorbenjensen/api-test",
    packages=["api_test"],
    scripts=['scripts/create_tables'],
    install_requires=[
        "fastapi",
        "psycopg2-binary",
        "python-dotenv",
        "pytz",
        "requests",
        "sqlalchemy",
        "sqlsoup",
        "uvicorn",
        # dev
        "black",
        "flake8",
        "rope",
    ],
)
