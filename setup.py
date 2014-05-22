from distutils.core import setup

VERSION = '0.1'

desc = """Remote Query Manager"""

name = 'requem'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['requem', 'requem.commands', 'requem.http', 'requem.remote_pool', 'requem.remote_queue',
                  'requem.zeromq'],
      platforms=['Any'],
      requires=['pyzmq', 'web.py', 'quecco']
)