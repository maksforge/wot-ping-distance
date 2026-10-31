"""Runs the patch against a stand-in for the game's AreaStaticMarkerPlugin (Python 2.7 or 3)."""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'res', 'scripts', 'client', 'gui', 'mods'))
sys.modules['debug_utils'] = types.ModuleType('debug_utils')
sys.modules['debug_utils'].LOG_CURRENT_EXCEPTION = lambda: None
sys.modules['debug_utils'].LOG_NOTE = lambda *a: None

import mod_maksforge_ping_distance as mod


class FakeMarker(object):

    def __init__(self, marker_id):
        self.marker_id = marker_id
        self.sticky = False

    def getMarkerID(self):
        return self.marker_id

    def getIsSticky(self):
        return self.sticky

    def setIsSticky(self, value):
        self.sticky = value


class AreaStaticMarkerPlugin(object):

    def __init__(self):
        self._markers = {}
        self.sticky_calls = []

    def _setMarkerSticky(self, markerID, isSticky):
        self.sticky_calls.append((markerID, isSticky))

    def __onStaticMarkerAdded(self, areaID, creatorID, position, subtype, markerText='', replies=0, isTarget=False):
        self._markers[areaID] = FakeMarker(100 + areaID)

    def __makeMarkerSticky(self, targetID, setSticky):
        marker = self._markers[targetID]
        self._setMarkerSticky(marker.getMarkerID(), setSticky)
        marker.setIsSticky(setSticky)

    def add(self, area_id):
        self.__onStaticMarkerAdded(area_id, 1, (0, 0, 0), 'attention_to')

    def focus(self, area_id, value):
        self.__makeMarkerSticky(area_id, value)


mod.patch(AreaStaticMarkerPlugin)


class PatchTest(unittest.TestCase):

    def test_new_ping_becomes_sticky(self):
        plugin = AreaStaticMarkerPlugin()
        plugin.add(7)
        self.assertEqual(plugin.sticky_calls, [(107, True)])
        self.assertTrue(plugin._markers[7].getIsSticky())

    def test_losing_focus_keeps_ping_sticky(self):
        plugin = AreaStaticMarkerPlugin()
        plugin.add(7)
        plugin.focus(7, False)
        self.assertEqual(plugin.sticky_calls[-1], (107, True))
        self.assertTrue(plugin._markers[7].getIsSticky())


if __name__ == '__main__':
    unittest.main()
