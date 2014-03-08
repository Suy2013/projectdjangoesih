#!/usr/bin/env python
import os
import sys
import sys
sys.path.append('/opt/Django')
import django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectesih.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
