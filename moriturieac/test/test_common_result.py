# -*- Mode: Python; test-case-name: moriturieac.test.test_common_result -*-

import os
import unittest

from morituri.image import toc
from morituri.result import result

from moriturieac.common import result as cresult

from morituri.test import common

class PixiesTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = cresult.EACLogger(frompath=u'/tmp')
        self.result = result.RipResult()
        self.result.artist = 'Pixies'
        self.result.title = 'Planet of Sound'
        self.result.offset = 102

        self.result.vendor = 'MATSHITA'
        self.result.model = 'DVD/CDRW UJDA775'

        tocfile = toc.TocFile(os.path.join(os.path.dirname(__file__),
            u'pixies.toc'))
        tocfile.parse()
        self.result.table = tocfile.table


        self.result.tracks.append(self._track(
            1, 'Pixies - Planet of Sound/01. Pixies - Planet of Sound.flac',
            12, 0.622, 0x14d38ce0, 0xca121fb9, 7))
        self.result.tracks.append(self._track(
            2, 'Pixies - Planet of Sound/02. Pixies - Theme from Narc.flac',
            145, 0.625, 0x4493ea28, 0xd05b2ce9, 8))
        self.result.tracks.append(self._track(
            3, 'Pixies - Planet of Sound/03. Pixies - Build High.flac',
            72, 0.526, 0x157099ed, 0x83507b5e, 8))
        self.result.tracks.append(self._track(
            4, 'Pixies - Planet of Sound/04. Pixies - Evil Hearted You.flac',
            70, 0.683, 0x7462c71b, 0x39b9c184, 8))

    def _track(self, n, filename, pregap, peak, crc, arcrc, arc):
        track = result.TrackResult()

        track.number = n
        track.filename = '/tmp/' + filename
        track.pregap = pregap

        track.peak = peak
        track.testcrc = track.copycrc = crc

        track.accurip = True
        track.ARCRC = track.ARDBCRC = arcrc
        track.ARDBConfidence = arc

        return track

        
    def testLog(self):
        result = self.logger.log(self.result, epoch=1243781200)
        path = os.path.join(os.path.dirname(__file__), 'pixies.eac.log')
        expected = open(path).read()
        common.diffStrings(result, expected)


