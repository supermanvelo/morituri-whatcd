# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

from setuptools import setup, find_packages

setup(
  name="morituri-whatcd",
  version="0.2.0",
  description="""morituri what.cd-style logger""",
  author="superveloman",
  packages=['morituriwhatcd', 'morituriwhatcd.logger', 'morituriwhatcd.test'],
  entry_points="""
  [morituri.logger]
  whatcd = morituriwhatcd.logger.whatcd:WhatCDLogger
  """)
