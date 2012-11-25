# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

from setuptools import setup, find_packages

setup(
  name="morituri-eac",
  version="0.0",
  description="""morituri EAC-style logger""",
  author="superveloman",
  packages=['moriturieac', 'moriturieac.logger', 'moriturieac.test'],
  entry_points="""
  [morituri.logger]
  eac0.99 = moriturieac.logger.eac099:EACLogger
  """)
