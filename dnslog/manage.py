#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing
import logger


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnslog.settings')
    try:
        from django.core.management import execute_from_command_line
        if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
            p = multiprocessing.Process(target=logger.run)
            p.daemon = True
            p.start()
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
