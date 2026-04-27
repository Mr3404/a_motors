# import os
# import sys

# path = '/home/mr3404/a_motors'
# if path not in sys.path:
#     sys.path.insert(0, path)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()