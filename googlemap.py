"""
Modyfikacja klasy z biblioteki gmplot, aby wykorzystywala nowe API Google Maps narzucajace korzystanie z klucza licencyjnego
"""

from gmplot import (GoogleMapPlotter)

class GoogleMapPlotterKey(GoogleMapPlotter):
    def draw(self, htmlfile):
        f = open(htmlfile, 'w')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write(
            '<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
        f.write(
            '<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
        f.write('<title>Google Maps - pygmaps </title>\n')
        # f.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization"></script>\n')
        f.write(
            '<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyASb3-xTdaXx05eFs6qbVV-hHMRENPEnuA"type="text/javascript"></script>')
        f.write('<script type="text/javascript">\n')
        f.write('\tfunction initialize() {\n')
        self.write_map(f)
        self.write_grids(f)
        self.write_points(f)
        self.write_paths(f)
        self.write_shapes(f)
        self.write_heatmap(f)
        f.write('\t}\n')
        f.write('</script>\n')
        f.write('</head>\n')
        f.write(
            '<body style="margin:0px; padding:0px;" onload="initialize()">\n')
        f.write(
            '\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
        f.write('</body>\n')
        f.write('</html>\n')
        f.close()