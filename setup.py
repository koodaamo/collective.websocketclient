from setuptools import setup, find_packages
import os

version = '1.2rc0'

setup(name='collective.websocketclient',
      version=version,
      description="Configure, open & maintain a persistent websocket connection in Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='websocket',
      author='Petri Savolainen',
      author_email='petri.savolainen@koodaamo.fi',
      url='https://github.com/koodaamo/collective.websocketclient',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'websocket-client'
          # -*- Extra requirements: -*-
      ],
      tests_require=[
         'websocket-server'
      ],
      extras_require = {
          'test': [
             'plone.app.testing',
             'websocket-server'
          ]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
