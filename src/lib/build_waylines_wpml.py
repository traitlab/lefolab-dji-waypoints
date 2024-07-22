import csv
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString

from lib.config import config


class BuildWaylinesWPML:

    def __init__(self):

        self.points_csv_properties = None

        # Find the Folder element containing Placemarks
        self.namespaces = {
            'kml': "http://www.opengis.net/kml/2.2",
            'wpml': "http://www.dji.com/wpmz/1.0.6"
        }

    def read_points_csv(self, csv_file):
        properties = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                lon = row['lon_x']
                lat = row['lat_y']
                height_ellipsoidal = row['elevation_from_dsm']
                polygon_id = row['polygon_id']
                properties.append((lat, lon, height_ellipsoidal, polygon_id))

        # Check if the first and last points are the same and remove the last point if they are
        if len(properties) > 1 and properties[0] == properties[-1]:
            properties.pop()

        return properties

    def setup(self):
        # Read the coordinates from the CSV
        self.points_csv_properties = self.read_points_csv(
            config.points_csv_file_path)

        # Register namespaces and parse the KML file
        ET.register_namespace('', "http://www.opengis.net/kml/2.2")
        ET.register_namespace('wpml', "http://www.dji.com/wpmz/1.0.6")
        self.tree = ET.parse(config.wpml_model_file_path)
        self.root = self.tree.getroot()

        self.folder = self.root.find('.//kml:Folder', self.namespaces)

        # Remove existing Placemark elements
        for placemark in self.folder.findall('kml:Placemark', self.namespaces):
            self.folder.remove(placemark)

    def generate(self):
        # Add new Placemark elements for each coordinate
        for idx, (lat, lon, height_ellipsoidal, polygon_id) in enumerate(self.points_csv_properties):
            index = idx * 4
            height = str(
                float(config.flight_height) - float(config.takeoff_point_elevation) + float(config.point_dsm_height_buffer))
            self.addPlacemarkStopNoAction(
                index, lat, lon, height)
            height = str(
                (float(height_ellipsoidal) - float(config.takeoff_point_elevation)) + float(config.point_dsm_height_buffer) + float(config.point_dsm_height_approach))
            self.addPlacemarkStopNoAction(
                index + 1, lat, lon, height)
            self.addPlacemarkWithActions(
                index + 2, lat, lon, height_ellipsoidal, polygon_id)
            height = str(
                float(config.flight_height) - float(config.takeoff_point_elevation) + float(config.point_dsm_height_buffer))
            self.addPlacemarkStopNoAction(
                index + 3, lat, lon, height)

    def addPlacemarkStopNoAction(self, idx, lat, lon, height):
        placemark = ET.Element(f'{{{self.namespaces["kml"]}}}Placemark')

        point = ET.SubElement(placemark, f'{{{self.namespaces["kml"]}}}Point')
        coordinates_element = ET.SubElement(
            point, f'{{{self.namespaces["kml"]}}}coordinates')
        coordinates_element.text = f'{lon},{lat}'

        wpml_index = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}index')
        wpml_index.text = str(idx)

        wpml_execute_height = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}executeHeight')
        wpml_execute_height.text = height

        # Load properties from JSON file
        with open('./config/waylines_placemark_no_action.json') as json_file:
            properties = json.load(json_file)

        # Add other properties from JSON file
        for prop, value in properties.items():
            if prop in ['coordinates', 'index', 'executeHeight']:
                continue
            self.addProperty(placemark, prop, value)

        self.folder.append(placemark)

    def addProperty(self, parent_elem, key, value):
        if isinstance(value, dict):
            # If value is a dictionary, create a sub-element and recursively call addProperty
            sub_elem = ET.SubElement(
                parent_elem, f'{{{self.namespaces["wpml"]}}}{key}')
            for sub_key, sub_value in value.items():
                self.addProperty(sub_elem, sub_key, sub_value)
        else:
            # If value is not a dictionary, add it as a subelement
            prop_elem = ET.SubElement(
                parent_elem, f'{{{self.namespaces["wpml"]}}}{key}')
            prop_elem.text = str(value)

    def addPlacemarkAction(self, parent, action, polygon_id):
        action_elem = ET.SubElement(
            parent, f'{{{self.namespaces["wpml"]}}}action')

        action_id = ''

        for key, value in action.items():
            if key == 'actionId':
                action_child_elem = ET.SubElement(action_elem, f'wpml:{key}')
                action_child_elem.text = value

                action_id = value

            elif key == 'actionActuatorFuncParam':
                params_elem = ET.SubElement(
                    action_elem, f'{{{self.namespaces["wpml"]}}}actionActuatorFuncParam')
                for param_key, param_value in value.items():
                    if param_key == 'orientedFileSuffix':
                        wpml_oriented_file_suffix = ET.SubElement(
                            params_elem, f'{{{self.namespaces["wpml"]}}}orientedFileSuffix')
                        wpml_oriented_file_suffix.text = f'action{action_id}_' + str(
                            polygon_id)
                    else:
                        param_elem = ET.SubElement(
                            params_elem, f'{{{self.namespaces["wpml"]}}}{param_key}')
                        param_elem.text = param_value
            else:
                action_child_elem = ET.SubElement(action_elem, f'wpml:{key}')
                action_child_elem.text = value

    def addPlacemarkActionGroup(self, idx, action_group, polygon_id):
        action_group_elem = ET.Element(
            f'{{{self.namespaces["wpml"]}}}actionGroup')
        for key, value in action_group.items():
            if key == 'actions':
                for action in value:
                    self.addPlacemarkAction(
                        action_group_elem, action, polygon_id)
            elif key == 'actionGroupStartIndex':
                actionGroupStartIndex = ET.SubElement(
                    action_group_elem, f'{{{self.namespaces["wpml"]}}}actionGroupStartIndex')
                actionGroupStartIndex.text = str(idx)
            elif key == 'actionGroupEndIndex':
                actionGroupEndIndex = ET.SubElement(
                    action_group_elem, f'{{{self.namespaces["wpml"]}}}actionGroupEndIndex')
                actionGroupEndIndex.text = str(idx)
            else:
                self.addProperty(action_group_elem, key, value)
                # action_group_child_elem = ET.SubElement(
                #     action_group_elem, f'{{{self.namespaces["wpml"]}}}{key}')
                # action_group_child_elem.text = value
        return action_group_elem

    def addPlacemarkWithActions(self, idx, lat, lon, height_ellipsoidal, polygon_id):
        placemark = ET.Element(f'{{{self.namespaces["kml"]}}}Placemark')

        point = ET.SubElement(placemark, f'{{{self.namespaces["kml"]}}}Point')
        coordinates_element = ET.SubElement(
            point, f'{{{self.namespaces["kml"]}}}coordinates')
        coordinates_element.text = f'{lon},{lat}'

        wpml_index = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}index')
        wpml_index.text = str(idx)

        wpml_execute_height = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}executeHeight')
        wpml_execute_height.text = str(
            (float(height_ellipsoidal) - float(config.takeoff_point_elevation)) + float(config.point_dsm_height_buffer))

        # Load properties from JSON file
        with open('./config/waylines_placemark_with_actions.json') as json_file:
            properties = json.load(json_file)

        # Other attributes
        for key, value in properties.items():
            if key in ['coordinates', 'index', 'executeHeight']:
                continue
            if key == 'actionGroups':
                for action_group in value:
                    action_group_elem = self.addPlacemarkActionGroup(idx,
                                                                     action_group, polygon_id)
                    placemark.append(action_group_elem)
            else:
                child_elem = ET.SubElement(
                    placemark, f'{{{self.namespaces["wpml"]}}}{key}')
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        sub_child_elem = ET.SubElement(
                            child_elem, f'{{{self.namespaces["wpml"]}}}{sub_key}')
                        sub_child_elem.text = sub_value
                else:
                    child_elem.text = value

        self.folder.append(placemark)

    def saveNewWPML(self):
        # Reopen, beautify it, and save it
        pretty_xml_str = self.beautify_xml()

        # Save the updated KML file
        wpml_path = Path(config.base_path) / config.base_name / \
            config.output_wpml_file_path

        os.makedirs(os.path.dirname(
            wpml_path), exist_ok=True)
        with open(wpml_path, 'w', encoding='utf-8') as file:
            file.write(pretty_xml_str)

    def beautify_xml(self):

        # Convert the XML tree to a string
        xml_str = ET.tostring(self.tree.getroot(),
                              encoding='utf-8', xml_declaration=True)

        # Parse the XML string
        dom = parseString(xml_str)

        # Pretty print the XML with an indentation of 2 spaces
        pretty_xml_str = dom.toprettyxml(
            indent="  ", encoding='utf-8').decode('utf-8')

        # Remove empty lines
        non_empty_lines = [
            line for line in pretty_xml_str.splitlines() if line.strip() != ""]
        cleaned_pretty_xml_str = "\n".join(non_empty_lines)

        return cleaned_pretty_xml_str
