import csv
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom.minidom import parseString

from lib.config import config


class BuildTemplateKML:

    # -------------------------------------------------------------------------
    def __init__(self):

        self.points_csv_properties = None

        # Stop placemark
        self.stop_use_global_speed = '1'
        self.stop_use_global_heading_param = '1'
        self.stop_use_global_turn_param = '1'
        self.stop_gimbal_pitch_angle = '-90'
        self.stop_use_straight_line = '0'
        self.stop_is_risky = '0'

        # Variables for common values
        # self.ellipsoid_height = '380.736267089844' # read from the CSV
        self.height = str(config.flight_height)  # '413.501159667969'
        # self.waypoint_speed = '5'
        # self.waypoint_heading_mode = 'fixed'
        # self.waypoint_heading_angle = '-52'
        # self.waypoint_poi_point = '0.000000,0.000000,0.000000'
        # self.waypoint_heading_path_mode = 'followBadArc'
        # self.waypoint_heading_poi_index = '0'
        self.use_global_speed = '1'
        self.use_global_heading_param = '1'
        self.use_global_turn_param = '1'
        self.gimbal_pitch_angle = '-90'
        self.use_straight_line = '0'

        self.action_group_id = '0'
        self.action_group_start_index = '0'
        self.action_group_end_index = '0'
        self.action_group_mode = 'sequence'
        self.action_trigger_type = 'reachPoint'

        # self.action_id = '0'
        self.action_actuator_func = 'orientedShoot'
        self.gimbal_pitch_rotate_angle = '-90'
        self.gimbal_roll_rotate_angle = '0'
        self.gimbal_yaw_rotate_angle = '-52.6846771240234'
        self.focus_x = '0'
        self.focus_y = '0'
        self.focus_region_width = '0'
        self.focus_region_height = '0'
        # self.focal_length = '24'
        self.aircraft_heading = '-52'
        self.accurate_frame_valid = '0'
        self.payload_position_index = '0'
        self.use_global_payload_lens_index = '0'
        self.target_angle = '0'
        # self.action_uuid = 'b67be2ca-9735-40bc-ab94-e9e01601e114'
        self.image_width = '0'
        self.image_height = '0'
        self.af_pos = '0'
        self.gimbal_port = '0'
        self.oriented_camera_type = '67'
        # self.oriented_file_path = '0c6f31bb-81bc-452d-904f-f15c5b92e330'
        # self.oriented_file_md5 = ''
        self.oriented_file_size = '0'
        # self.oriented_file_suffix = 'Waypoint1'
        self.oriented_photo_mode = 'normalPhoto'
        # self.action_actuator_func2 = 'rotateYaw'
        # self.aircraft_heading2 = '-51'
        # self.aircraft_path_mode = 'counterClockwise'
        self.is_risky = '0'
        # Define namespaces
        self.namespaces = {
            'kml': 'http://www.opengis.net/kml/2.2',
            'wpml': 'http://www.dji.com/wpmz/1.0.6'
        }

    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    def setup(self):
        # Read the coordinates from the CSV
        self.points_csv_properties = self.read_points_csv(
            config.points_csv_file_path)

        # Register namespaces and parse the KML file
        ET.register_namespace('', "http://www.opengis.net/kml/2.2")
        ET.register_namespace('wpml', "http://www.dji.com/wpmz/1.0.6")

        # Parse the KML file
        self.tree = ET.parse(config.kml_model_file_path)
        self.root = self.tree.getroot()

        # Find the Folder element
        self.folder = self.root.find('.//kml:Folder', self.namespaces)
        # Remove all existing Placemark elements with Point
        for placemark in self.folder.findall('kml:Placemark', self.namespaces):
            self.folder.remove(placemark)

    # -------------------------------------------------------------------------
    def generate(self):
        # Add new Placemark elements for each coordinate
        for idx, (lat, lon, height_ellipsoidal, polygon_id) in enumerate(self.points_csv_properties):
            index = idx * 4
            height = str(
                float(config.flight_height) - float(config.takeoff_point_elevation) + float(config.point_dsm_height_buffer))
            self.addPlacemarkStop(
                index, lat, lon, height, polygon_id)
            height = str(
                (float(height_ellipsoidal) -
                 float(config.takeoff_point_elevation)) + float(config.point_dsm_height_buffer) + float(config.point_dsm_height_approach))
            self.addPlacemarkStop(
                index + 1, lat, lon, height, polygon_id)
            self.addPlacemarkActions(
                index + 2, lat, lon, height_ellipsoidal, polygon_id)
            height = str(
                float(config.flight_height) - float(config.takeoff_point_elevation) + float(config.point_dsm_height_buffer))
            self.addPlacemarkStop(
                index + 3, lat, lon, height, polygon_id)

    # -------------------------------------------------------------------------
    def addPlacemarkStop(self, idx, lat, lon, height, polygon_id):
        # Add new Placemark elements for each coordinate
        # for idx, (lat, lon, height_ellipsoidal, polygon_id) in enumerate(self.csv_properties):
        placemark = ET.Element(f'{{{self.namespaces["kml"]}}}Placemark')

        point = ET.SubElement(placemark, f'{{{self.namespaces["kml"]}}}Point')
        coordinates_element = ET.SubElement(
            point, f'{{{self.namespaces["kml"]}}}coordinates')
        coordinates_element.text = f'{lon},{lat}'

        wpml_index = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}index')
        wpml_index.text = str(idx)

        wpml_ellipsoidHeight = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}ellipsoidHeight')
        wpml_ellipsoidHeight.text = height

        wpml_height = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}height')
        wpml_height.text = height

        wpml_use_global_speed = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalSpeed')
        wpml_use_global_speed.text = self.stop_use_global_speed

        wpml_use_global_heading_param = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalHeadingParam')
        wpml_use_global_heading_param.text = self.stop_use_global_heading_param

        wpml_use_global_turn_param = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalTurnParam')
        wpml_use_global_turn_param.text = self.stop_use_global_turn_param

        # wpml_gimbal_pitch_angle = ET.SubElement(
        #     placemark, f'{{{self.namespaces["wpml"]}}}gimbalPitchAngle')
        # wpml_gimbal_pitch_angle.text = self.stop_gimbal_pitch_angle

        wpml_use_straight_line = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useStraightLine')
        wpml_use_straight_line.text = self.stop_use_straight_line

        wpml_is_risky = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}isRisky')
        wpml_is_risky.text = self.stop_is_risky

        ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}orientedFileSuffix').text = polygon_id

        self.folder.append(placemark)

    # -------------------------------------------------------------------------
    def addPlacemarkActionGroup(self, index):
        action_group = ET.Element(f'{{{self.namespaces["wpml"]}}}actionGroup')
        ET.SubElement(
            action_group, f'{{{self.namespaces["wpml"]}}}actionGroupId').text = self.action_group_id
        ET.SubElement(
            action_group, f'{{{self.namespaces["wpml"]}}}actionGroupStartIndex').text = str(index)
        ET.SubElement(
            action_group, f'{{{self.namespaces["wpml"]}}}actionGroupEndIndex').text = str(index)
        ET.SubElement(
            action_group, f'{{{self.namespaces["wpml"]}}}actionGroupMode').text = self.action_group_mode

        action_trigger = ET.SubElement(
            action_group, f'{{{self.namespaces["wpml"]}}}actionTrigger')
        ET.SubElement(
            action_trigger, f'{{{self.namespaces["wpml"]}}}actionTriggerType').text = self.action_trigger_type

        return action_group

    # -------------------------------------------------------------------------
    def addPlacemarkAction(self, idx, focalLength, orientedFileSuffix, actionUUID, orientedFilePath):
        action = ET.Element(f'{{{self.namespaces["wpml"]}}}action')
        ET.SubElement(
            action, f'{{{self.namespaces["wpml"]}}}actionId').text = idx
        ET.SubElement(
            action, f'{{{self.namespaces["wpml"]}}}actionActuatorFunc').text = self.action_actuator_func

        action_actuator_func_param = ET.SubElement(
            action, f'{{{self.namespaces["wpml"]}}}actionActuatorFuncParam')
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}gimbalPitchRotateAngle').text = self.gimbal_pitch_rotate_angle
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}gimbalRollRotateAngle').text = self.gimbal_roll_rotate_angle
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}gimbalYawRotateAngle').text = self.gimbal_yaw_rotate_angle
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}focusX').text = self.focus_x
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}focusY').text = self.focus_y
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}focusRegionWidth').text = self.focus_region_width
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}focusRegionHeight').text = self.focus_region_height
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}focalLength').text = focalLength
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}aircraftHeading').text = self.aircraft_heading
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}accurateFrameValid').text = self.accurate_frame_valid
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}payloadPositionIndex').text = self.payload_position_index
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}useGlobalPayloadLensIndex').text = self.use_global_payload_lens_index
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}targetAngle').text = self.target_angle
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}actionUUID').text = actionUUID
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}imageWidth').text = self.image_width
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}imageHeight').text = self.image_height
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}AFPos').text = self.af_pos
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}gimbalPort').text = self.gimbal_port
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedCameraType').text = self.oriented_camera_type
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedFilePath').text = orientedFilePath
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedFileMD5')
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedFileSize').text = self.oriented_file_size
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedFileSuffix').text = orientedFileSuffix
        ET.SubElement(action_actuator_func_param,
                      f'{{{self.namespaces["wpml"]}}}orientedPhotoMode').text = self.oriented_photo_mode

        return action

    # -------------------------------------------------------------------------
    def addPlacemarkActions(self, idx, lat, lon, height_ellipsoidal, polygon_id):
        placemark = ET.Element(f'{{{self.namespaces["kml"]}}}Placemark')

        point = ET.SubElement(placemark, f'{{{self.namespaces["kml"]}}}Point')
        coordinates_element = ET.SubElement(
            point, f'{{{self.namespaces["kml"]}}}coordinates')
        coordinates_element.text = f'{lon},{lat}'

        wpml_index = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}index')
        wpml_index.text = str(idx)

        wpml_ellipsoidHeight = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}ellipsoidHeight')
        wpml_ellipsoidHeight.text = str(
            (float(height_ellipsoidal) -
             float(config.takeoff_point_elevation)) + float(config.point_dsm_height_buffer))

        wpml_height = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}height')
        wpml_height.text = str(
            (float(height_ellipsoidal) -
             float(config.takeoff_point_elevation)) + float(config.point_dsm_height_buffer))

        wpml_useGlobalSpeed = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalSpeed')
        wpml_useGlobalSpeed.text = self.use_global_speed

        wpml_useGlobalHeadingParam = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalHeadingParam')
        wpml_useGlobalHeadingParam.text = self.use_global_heading_param

        wpml_useGlobalTurnParam = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useGlobalTurnParam')
        wpml_useGlobalTurnParam.text = self.use_global_turn_param

        # wpml_gimbalPitchAngle = ET.SubElement(
        #     placemark, f'{{{self.namespaces["wpml"]}}}gimbalPitchAngle')
        # wpml_gimbalPitchAngle.text = self.gimbal_pitch_angle

        wpml_useStraightLine = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}useStraightLine')
        wpml_useStraightLine.text = self.use_straight_line

        wpml_isRisky = ET.SubElement(
            placemark, f'{{{self.namespaces["wpml"]}}}isRisky')
        wpml_isRisky.text = self.is_risky

        wpml_actionGroup = self.addPlacemarkActionGroup(idx)
        placemark.append(wpml_actionGroup)

        wpml_action = self.addPlacemarkAction('1', '168', str(
            polygon_id) + "zoom", '703556e4-81fb-4294-b607-05d5f748377f', '703556e4-81fb-4294-b607-05d5f748377f')
        wpml_actionGroup.append(wpml_action)

        wpml_action = self.addPlacemarkAction('0', '24', str(
            polygon_id), '51ae7825-56de-41d3-90bb-3c9ed6de7960', '393e34ba-016e-4fd3-98bf-3f9fe0c517df')
        wpml_actionGroup.append(wpml_action)

        self.folder.append(placemark)

    # -------------------------------------------------------------------------
    def saveNewKML(self):
        # Reopen, beautify it, and save it
        pretty_xml_str = self.beautify_xml()

        # Save the updated KML file
        kml_path = Path(config.base_path) / config.base_name / \
            config.output_kml_file_path
        os.makedirs(os.path.dirname(
            kml_path), exist_ok=True)
        with open(kml_path, 'w', encoding='UTF-8') as file:
            file.write(pretty_xml_str)

    # -------------------------------------------------------------------------
    def beautify_xml(self):

        # Convert the XML tree to a string
        xml_str = ET.tostring(self.tree.getroot(), encoding='unicode')

        # Parse the XML string
        dom = parseString(xml_str)

        # Pretty print the XML with an indentation of 2 spaces
        pretty_xml_str = dom.toprettyxml(indent="  ")

        # Remove empty lines
        non_empty_lines = [
            line for line in pretty_xml_str.splitlines() if line.strip() != ""]
        cleaned_pretty_xml_str = "\n".join(non_empty_lines)

        return cleaned_pretty_xml_str
