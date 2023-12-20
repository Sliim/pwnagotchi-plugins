import logging
import pwnagotchi.grid as grid
import pwnagotchi.plugins as plugins


class GPSGrid(plugins.Plugin):
    __author__ = "sliim@mailoo.org"
    __version__ = "1.0.0"
    __license__ = "GPL3"
    __description__ = """
    Share GPS coordinates with grid.
    Requires gps plugin enabled.
    """

    def __init__(self):
        self.gps = None
        self.coordinates = None

    def _coords(self):
        if self.gps and self.gps.running:
            coordinates = self.gps.coordinates
            if coordinates \
               and all([coordinates["Latitude"], coordinates["Longitude"]]):
                return coordinates
        return None

    def on_loaded(self):
        try:
            logging.info("[gps_grid] plugin loaded")
        except Exception as e:
            logging.error("gps_grid.on_loaded: %s" % e)

    def on_ready(self, agent):
        try:
            self.gps = plugins.loaded["gps"]
            if not self.gps:
                logging.error("[gps_grid] gps plugin not loaded!")
        except Exception as e:
            logging.error("gps_grid.on_ready: %s" % e)

    def on_epoch(self, agent, epoch, data):
        try:
            coords = self._coords()
            if coords and coords != self.coordinates:
                grid.call("/mesh/data", {"coordinates": coords})
                self.coordinates = coords
        except Exception as e:
            logging.error("gps_grid.on_epoch: %s" % e)
