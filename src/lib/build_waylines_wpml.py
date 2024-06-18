import csv
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from lib.config import config


class BuildWaylinesWPML:

    def __init__(self):
        self.execute_height = '380.736267089844'
        self.waypoint_speed = '5'
        self.waypoint_heading_mode = 'fixed'
        self.waypoint_heading_angle = '-52'
        self.waypoint_heading_poi_point = '0.000000,0.000000,0.000000'
        self.waypoint_heading_angle_enable = '0'
        self.waypoint_heading_path_mode = 'followBadArc'
        self.waypoint_heading_poi_index = '0'
        self.waypoint_turn_mode = 'toPointAndStopWithDiscontinuityCurvature'
        self.waypoint_turn_damping_dist = '0'
        self.use_straight_line = '1'
        self.action_group_id = '0'
        self.action_group_start_index = '0'
        self.action_group_end_index = '0'
        self.action_group_mode = 'sequence'
        self.action_trigger_type = 'reachPoint'
        self.action_id = '0'
        self.action_actuator_func = 'orientedShoot'
        self.gimbal_pitch_rotate_angle = '-90'
        self.gimbal_roll_rotate_angle = '0'
        self.gimbal_yaw_rotate_angle = '-52.6846771240234'
        self.focus_x = '0'
        self.focus_y = '0'
        self.focus_region_width = '0'
        self.focus_region_height = '0'
        self.focal_length = '24'
        self.aircraft_heading = '-52'
        self.accurate_frame_valid = '0'
        self.payload_position_index = '0'
        self.use_global_payload_lens_index = '0'
        self.target_angle = '0'
        self.action_uuid = 'b67be2ca-9735-40bc-ab94-e9e01601e114'
        self.image_width = '0'
        self.image_height = '0'
        self.af_pos = '0'
        self.gimbal_port = '0'
        self.oriented_camera_type = '67'
        self.oriented_file_path = '0c6f31bb-81bc-452d-904f-f15c5b92e330'
        self.oriented_file_md5 = ''
        self.oriented_file_size = '0'
        # self.oriented_file_suffix = 'Waypoint1'
        self.oriented_photo_mode = 'normalPhoto'
        self.is_risky = '0'
        self.waypoint_work_type = '0'
        self.waypoint_gimbal_pitch_angle = '0'
        self.waypoint_gimbal_yaw_angle = '0'

        # Find the Folder element containing Placemarks
        self.namespaces = {
            'kml': "http://www.opengis.net/kml/2.2",
            'wpml': "http://www.dji.com/wpmz/1.0.6"
        }

    def read_coordinates_from_csv(self, csv_file):
        coordinates = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                lat = row['latitude']
                lon = row['longitude']
                height_ellipsoidal = row['elevation_from_dsm']
                polygon_id = row['polygon_id']
                coordinates.append((lat, lon, height_ellipsoidal, polygon_id))
        return coordinates

    def setup(self):
        # Read the coordinates from the CSV
        self.coordinates = self.read_coordinates_from_csv(
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

    def addNewPlacemark(self):

        # Create new Placemark elements based on the CSV coordinates
        for index, (lat, lon, height_ellipsoidal, polygon_id) in enumerate(self.coordinates):
            placemark = ET.Element(f'{{{self.namespaces["kml"]}}}Placemark')

            point = ET.SubElement(
                placemark, f'{{{self.namespaces["kml"]}}}Point')
            coordinates_element = ET.SubElement(
                point, f'{{{self.namespaces["kml"]}}}coordinates')
            coordinates_element.text = f'{lat},{lon}'

            wpml_index = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}index')
            wpml_index.text = str(index)

            wpml_executeHeight = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}executeHeight')
            wpml_executeHeight.text = height_ellipsoidal

            wpml_waypointSpeed = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}waypointSpeed')
            wpml_waypointSpeed.text = self.waypoint_speed

            wpml_waypointHeadingParam = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}waypointHeadingParam')
            wpml_waypointHeadingMode = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointHeadingMode')
            wpml_waypointHeadingMode.text = self.waypoint_heading_mode
            wpml_waypointHeadingAngle = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointHeadingAngle')
            wpml_waypointHeadingAngle.text = self.waypoint_heading_angle
            wpml_waypointPoiPoint = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointPoiPoint')
            wpml_waypointPoiPoint.text = self.waypoint_heading_poi_point
            wpml_waypointHeadingAngleEnable = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointHeadingAngleEnable')
            wpml_waypointHeadingAngleEnable.text = self.waypoint_heading_angle_enable
            wpml_waypointHeadingPathMode = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointHeadingPathMode')
            wpml_waypointHeadingPathMode.text = self.waypoint_heading_path_mode
            wpml_waypointHeadingPoiIndex = ET.SubElement(
                wpml_waypointHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointHeadingPoiIndex')
            wpml_waypointHeadingPoiIndex.text = self.waypoint_heading_poi_index

            wpml_waypointTurnParam = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}waypointTurnParam')
            wpml_waypointTurnMode = ET.SubElement(
                wpml_waypointTurnParam, f'{{{self.namespaces["wpml"]}}}waypointTurnMode')
            wpml_waypointTurnMode.text = self.waypoint_turn_mode
            wpml_waypointTurnDampingDist = ET.SubElement(
                wpml_waypointTurnParam, f'{{{self.namespaces["wpml"]}}}waypointTurnDampingDist')
            wpml_waypointTurnDampingDist.text = self.waypoint_turn_damping_dist

            wpml_useStraightLine = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}useStraightLine')
            wpml_useStraightLine.text = self.use_straight_line

            wpml_actionGroup = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}actionGroup')
            wpml_actionGroupId = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}actionGroupId')
            wpml_actionGroupId.text = self.action_group_id
            wpml_actionGroupStartIndex = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}actionGroupStartIndex')
            wpml_actionGroupStartIndex.text = self.action_group_start_index
            wpml_actionGroupEndIndex = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}actionGroupEndIndex')
            wpml_actionGroupEndIndex.text = self.action_group_end_index
            wpml_actionGroupMode = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}actionGroupMode')
            wpml_actionGroupMode.text = self.action_group_mode

            wpml_actionTrigger = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}actionTrigger')
            wpml_actionTriggerType = ET.SubElement(
                wpml_actionTrigger, f'{{{self.namespaces["wpml"]}}}actionTriggerType')
            wpml_actionTriggerType.text = self.action_trigger_type

            wpml_action = ET.SubElement(
                wpml_actionGroup, f'{{{self.namespaces["wpml"]}}}action')
            wpml_actionId = ET.SubElement(
                wpml_action, f'{{{self.namespaces["wpml"]}}}actionId')
            wpml_actionId.text = self.action_id
            wpml_actionActuatorFunc = ET.SubElement(
                wpml_action, f'{{{self.namespaces["wpml"]}}}actionActuatorFunc')
            wpml_actionActuatorFunc.text = self.action_actuator_func

            wpml_actionActuatorFuncParam = ET.SubElement(
                wpml_action, f'{{{self.namespaces["wpml"]}}}actionActuatorFuncParam')
            wpml_gimbalPitchRotateAngle = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}gimbalPitchRotateAngle')
            wpml_gimbalPitchRotateAngle.text = self.gimbal_pitch_rotate_angle
            wpml_gimbalRollRotateAngle = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}gimbalRollRotateAngle')
            wpml_gimbalRollRotateAngle.text = self.gimbal_roll_rotate_angle
            wpml_gimbalYawRotateAngle = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}gimbalYawRotateAngle')
            wpml_gimbalYawRotateAngle.text = self.gimbal_yaw_rotate_angle
            wpml_focusX = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}focusX')
            wpml_focusX.text = self.focus_x
            wpml_focusY = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}focusY')
            wpml_focusY.text = self.focus_y
            wpml_focusRegionWidth = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}focusRegionWidth')
            wpml_focusRegionWidth.text = self.focus_region_width
            wpml_focusRegionHeight = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}focusRegionHeight')
            wpml_focusRegionHeight.text = self.focus_region_height
            wpml_focalLength = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}focalLength')
            wpml_focalLength.text = self.focal_length
            wpml_aircraftHeading = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}aircraftHeading')
            wpml_aircraftHeading.text = self.aircraft_heading
            wpml_accurateFrameValid = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}accurateFrameValid')
            wpml_accurateFrameValid.text = self.accurate_frame_valid
            wpml_payloadPositionIndex = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}payloadPositionIndex')
            wpml_payloadPositionIndex.text = self.payload_position_index
            wpml_useGlobalPayloadLensIndex = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}useGlobalPayloadLensIndex')
            wpml_useGlobalPayloadLensIndex.text = self.use_global_payload_lens_index
            wpml_targetAngle = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}targetAngle')
            wpml_targetAngle.text = self.target_angle
            wpml_actionUUID = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}actionUUID')
            wpml_actionUUID.text = self.action_uuid
            wpml_imageWidth = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}imageWidth')
            wpml_imageWidth.text = self.image_width
            wpml_imageHeight = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}imageHeight')
            wpml_imageHeight.text = self.image_height
            wpml_AFPos = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}AFPos')
            wpml_AFPos.text = self.af_pos
            wpml_gimbalPort = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}gimbalPort')
            wpml_gimbalPort.text = self.gimbal_port
            wpml_orientedCameraType = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedCameraType')
            wpml_orientedCameraType.text = self.oriented_camera_type
            wpml_orientedFilePath = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedFilePath')
            wpml_orientedFilePath.text = self.oriented_file_path
            wpml_orientedFileMD5 = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedFileMD5')
            wpml_orientedFileMD5.text = self.oriented_file_md5
            wpml_orientedFileSize = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedFileSize')
            wpml_orientedFileSize.text = self.oriented_file_size
            wpml_orientedFileSuffix = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedFileSuffix')
            wpml_orientedFileSuffix.text = polygon_id
            wpml_orientedPhotoMode = ET.SubElement(
                wpml_actionActuatorFuncParam, f'{{{self.namespaces["wpml"]}}}orientedPhotoMode')
            wpml_orientedPhotoMode.text = self.oriented_photo_mode

            wpml_waypointGimbalHeadingParam = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}waypointGimbalHeadingParam')
            wpml_waypointGimbalPitchAngle = ET.SubElement(
                wpml_waypointGimbalHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointGimbalPitchAngle')
            wpml_waypointGimbalPitchAngle.text = self.waypoint_gimbal_pitch_angle
            wpml_waypointGimbalYawAngle = ET.SubElement(
                wpml_waypointGimbalHeadingParam, f'{{{self.namespaces["wpml"]}}}waypointGimbalYawAngle')
            wpml_waypointGimbalYawAngle.text = self.waypoint_gimbal_yaw_angle

            wpml_isRisky = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}isRisky')
            wpml_isRisky.text = self.is_risky

            wpml_waypointWorkType = ET.SubElement(
                placemark, f'{{{self.namespaces["wpml"]}}}waypointWorkType')
            wpml_waypointWorkType.text = self.waypoint_work_type

            self.folder.append(placemark)

    def saveNewWPML(self):
        # Reopen, beautify it, and save it
        pretty_xml_str = self.beautify_xml()

        # Save the updated KML file
        os.makedirs(os.path.dirname(
            config.output_wpml_file_path), exist_ok=True)
        with open(config.output_wpml_file_path, 'w', encoding='UTF-8') as file:
            file.write(pretty_xml_str)

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
