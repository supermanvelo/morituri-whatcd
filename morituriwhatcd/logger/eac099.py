# -*- Mode: Python; test-case-name: moriturieac.test.test_logger_eac099 -*-

import os
import time

from morituri.common import common
from morituri.result import result

class EACLogger(result.Logger):

    def __init__(self, frompath=os.getcwd(), topath='D:\eac'):
        self._frompath = frompath
        self._topath = topath

    def _framesToMSF(self, frames):
        # format specifically for EAC log; examples:
        # 5:39.57
        f = frames % common.FRAMES_PER_SECOND
        frames -= f
        s = (frames / common.FRAMES_PER_SECOND) % 60
        frames -= s * 60
        m = frames / common.FRAMES_PER_SECOND / 60

        return "%2d:%02d.%02d" % (m, s, f)

    def _framesToHMSH(self, frames):
        # format specifically for EAC log; examples:
        # 0:00.00.70
        # FIXME: probably depends on General EAC setting (display as frames)
        # if this formats as frames or as hundreds of seconds
        f = frames % common.FRAMES_PER_SECOND
        frames -= f
        s = (frames / common.FRAMES_PER_SECOND) % 60
        frames -= s * 60
        m = frames / common.FRAMES_PER_SECOND / 60
        frames -= m * 60
        h = frames / common.FRAMES_PER_SECOND / 60 / 60

        #return "%2d:%02d:%02d.%02d" % (h, m, s, int((f / 75.0) * 100.0))
        return "%2d:%02d:%02d.%02d" % (h, m, s, f)


    def log(self, ripResult, epoch=time.time()):
        lines = self.logRip(ripResult, epoch=epoch)
        return '\r\n'.join(lines)


    def logRip(self, ripResult, epoch):

        lines = []

        ### global

        # version string; FIXME
        lines.append("Exact Audio Copy V0.99 prebeta 4 from 23. January 2008")
        lines.append("")

        # date when EAC writes the log file
        # using %e for day of month and strip because EAC formats like this:
        # 4. June 2009, 16:18
        # 6. September 2009, 9:14
        # %-H formats the hour with one digit only when it's one digit
        date = time.strftime("%e. %B %Y, %-H:%M", time.localtime(epoch)).strip()
        lines.append("EAC extraction logfile from %s" % date)
        lines.append("")

        # album
        lines.append("%s / %s" % (ripResult.artist, ripResult.title))
        lines.append("")

        # drive
        lines.append(
            "Used drive  : %s%s  Adapter: 1  ID: 0" % (
                ripResult.vendor, ripResult.model))
        lines.append("")

        # settings; FIXME
        lines.append("Read mode               : Secure")
        lines.append("Utilize accurate stream : Yes")
        lines.append("Defeat audio cache      : Yes")
        lines.append("Make use of C2 pointers : No")
 
        lines.append("")

        lines.append("Read offset correction                      : %d" %
            ripResult.offset)
        lines.append("Overread into Lead-In and Lead-Out          : No")
        lines.append("Fill up missing offset samples with silence : Yes")
        lines.append("Delete leading and trailing silent blocks   : No")
        lines.append("Null samples used in CRC calculations       : Yes")
        lines.append("Used interface                              : Installed external ASPI interface")
        lines.append("Gap handling                                : Appended to previous track")
        lines.append("")
        lines.append("Used output format              : User Defined Encoder")
        lines.append("Selected bitrate                : 128 kBit/s")
        lines.append("Quality                         : High")
        lines.append("Add ID3 tag                     : No")
        lines.append("Command line compressor         : C:\\Program Files\\Exact Audio Copy\\Flac\\flac.exe")
        lines.append('Additional command line options : -V -8 -T "artist=%a" -T "title=%t" -T "album=%g" -T "date=%y" -T "tracknumber=%n" -T "genre=%m" %s')
        lines.append("")
        lines.append("")

        # toc
        lines.append("TOC of the extracted CD")
        lines.append("")
        lines.append(
            "     Track |   Start  |  Length  | Start sector | End sector ")
        lines.append(
            "    ---------------------------------------------------------")
        table = ripResult.table


        for t in table.tracks:
            # FIXME: what happens to a track start over 60 minutes ?
            start = t.getIndex(1).absolute
            length = table.getTrackLength(t.number)
            end = table.getTrackEnd(t.number)
            lines.append(
            "       %2d  | %s | %s |    %6d    |   %6d   " % (
                t.number, 
                self._framesToMSF(start),
                self._framesToMSF(length),
                start, end))

        lines.append("")
        lines.append("")

        ### per-track
        for t in ripResult.tracks:
            lines.extend(self.trackLog(t))
            lines.append('')

        ### global overview
        # FIXME

        lines.append("")
        lines.append("All tracks accurately ripped")
        lines.append("")
        lines.append("No errors occurred")
        lines.append("")
        lines.append("End of status report")
        lines.append("")

        return lines

    def _filename(self, filename):
        # Convert the extension to .wav always
        (root, ext) = os.path.splitext(filename)
        filename = root + '.wav'

        # Convert the unix path to a windows path
        if filename.startswith(self._frompath):
            filename = self._topath + filename[len(self._frompath):]

        filename = "\\".join(filename.split("/"))

        return filename


    def trackLog(self, trackResult):

        lines = []

        lines.append('Track %2d' % trackResult.number)
        lines.append('')
        lines.append('     Filename %s' % self._filename(trackResult.filename))
        lines.append('')

        # EAC adds the 2 seconds to the first track pregap
        pregap = trackResult.pregap
        if trackResult.number == 1:
            pregap += 2 * common.FRAMES_PER_SECOND
        if pregap:
            lines.append('     Pre-gap length %s' % self._framesToHMSH(
                pregap))
            lines.append('')

        # EAC seems to format peak differently, truncating to the 3rd digit,
        # and also calculating it against a max of 32767
        # MBV - Feed me with your kiss: replaygain 0.809875,
        # EAC's peak level 80.9 % instead of 90.0 %
        peak = trackResult.peak * 32768 / 32767
        #lines.append('     Peak level %r' % peak)
        lines.append('     Peak level %.1f %%' % (
            int(peak * 1000) / 10.0))
        #level = "%.2f" % (trackResult.peak * 100.0)
        #level = level[:-1]
        #lines.append('     Peak level %s %%' % level)
        # Track quality is shown in secure mode
        if trackResult.quality and trackResult.quality > 0.001:
            lines.append('     Track quality %.1f %%' % (
                trackResult.quality * 100.0, ))
        if trackResult.testcrc is not None:
            lines.append('     Test CRC %08X' % trackResult.testcrc)
        if trackResult.copycrc is not None:
            lines.append('     Copy CRC %08X' % trackResult.copycrc)
        
        if trackResult.accurip:
            if trackResult.ARCRC == trackResult.ARDBCRC:
                lines.append('     Accurately ripped (confidence %d)  [%08X]' % (
                    trackResult.ARDBConfidence, trackResult.ARCRC))
            else:
                lines.append('     Cannot be verified as accurate  '
                    '(confidence %d),  [%08X], AccurateRip returned [%08x]' % (
                        trackResult.ARDBConfidence,
                        trackResult.ARCRC, trackResult.ARDBCRC))
        else:
            lines.append('     Track not present in AccurateRip database')

        if trackResult.testcrc == trackResult.copycrc:
            lines.append('     Copy OK')
        # FIXME: else ?
        return lines

