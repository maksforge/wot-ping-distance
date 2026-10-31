"""Keeps position pings sticky so the engine keeps drawing their distance, not only while aimed at."""
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_NOTE

_PLUGIN_PATH = 'gui.Scaleform.daapi.view.battle.shared.markers2d.plugins'
_ADDED = '_AreaStaticMarkerPlugin__onStaticMarkerAdded'
_MAKE_STICKY = '_AreaStaticMarkerPlugin__makeMarkerSticky'


def _stick(plugin, area_id):
    marker = plugin._markers.get(area_id)
    if marker is None or marker.getIsSticky():
        return
    plugin._setMarkerSticky(marker.getMarkerID(), True)
    marker.setIsSticky(True)


def patch(plugin_class):
    original_added = getattr(plugin_class, _ADDED)
    original_make_sticky = getattr(plugin_class, _MAKE_STICKY)

    def on_static_marker_added(self, areaID, *args, **kwargs):
        original_added(self, areaID, *args, **kwargs)
        try:
            _stick(self, areaID)
        except Exception:
            LOG_CURRENT_EXCEPTION()

    def make_marker_sticky(self, targetID, setSticky):
        original_make_sticky(self, targetID, True)

    setattr(plugin_class, _ADDED, on_static_marker_added)
    setattr(plugin_class, _MAKE_STICKY, make_marker_sticky)


def init():
    try:
        import importlib
        plugins = importlib.import_module(_PLUGIN_PATH)
        patch(plugins.AreaStaticMarkerPlugin)
        LOG_NOTE('[maksforge.ping_distance] position pings stay sticky')
    except Exception:
        LOG_CURRENT_EXCEPTION()
