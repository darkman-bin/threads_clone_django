#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'threader.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. تأكد أنك ثبّتت المتطلبات عبر pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
