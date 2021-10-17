#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# for deployment to app platform
import dotenv
import pathlib


def main():
    """Run administrative tasks."""
    # for deployment to app platform
    # DOT_ENV_PATH = pathlib.Path() / '.env'
    # if DOT_ENV_PATH.exists():
    #     dotenv.read_dotenv(str(DOT_ENV_PATH))
    # else:
    #     print('no .env file found')
    dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gradr.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
