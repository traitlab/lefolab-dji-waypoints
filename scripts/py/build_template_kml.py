import csv
import os
import xml.etree.ElementTree as ET


def read_coordinates_from_csv(csv_file):
    coordinates = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = row['latitude']
            lon = row['longitude']
            coordinates.append((lat, lon))
    return coordinates


# File paths
kml_file_path = './scripts/wpml/model/Waypoint2/wpmz/template.kml'
csv_file_path = 'waypoints.csv'
output_kml_file_path = './scripts/wpml/template.kml'

# Read the coordinates from the CSV
coordinates = read_coordinates_from_csv(csv_file_path)

# Register namespaces and parse the KML file
ET.register_namespace('', "http://www.opengis.net/kml/2.2")
ET.register_namespace('wpml', "http://www.dji.com/wpmz/1.0.6")

# Parse the KML file
tree = ET.parse(kml_file_path)
root = tree.getroot()

# Define namespaces
namespaces = {
    'kml': 'http://www.opengis.net/kml/2.2',
    'wpml': 'http://www.dji.com/wpmz/1.0.6'
}

# Find the Folder element
folder = root.find('.//kml:Folder', namespaces)

# Remove all existing Placemark elements with Point
for placemark in folder.findall('kml:Placemark', namespaces):
    folder.remove(placemark)

# Variables for common values
ellipsoid_height = '380.736267089844'
height = '413.501159667969'
waypoint_speed = '5'
waypoint_heading_mode = 'fixed'
waypoint_heading_angle = '-52'
waypoint_poi_point = '0.000000,0.000000,0.000000'
waypoint_heading_path_mode = 'followBadArc'
waypoint_heading_poi_index = '0'
use_global_turn_param = '1'
use_straight_line = '0'
action_group_id = '0'
action_group_start_index = '0'
action_group_end_index = '0'
action_group_mode = 'sequence'
action_trigger_type = 'reachPoint'
action_id = '0'
action_actuator_func = 'orientedShoot'
gimbal_pitch_rotate_angle = '-89.9000015258789'
gimbal_roll_rotate_angle = '0'
gimbal_yaw_rotate_angle = '-52.6846771240234'
focus_x = '0'
focus_y = '0'
focus_region_width = '0'
focus_region_height = '0'
focal_length = '24'
aircraft_heading = '-52'
accurate_frame_valid = '0'
payload_position_index = '0'
use_global_payload_lens_index = '0'
target_angle = '0'
action_uuid = 'b67be2ca-9735-40bc-ab94-e9e01601e114'
image_width = '0'
image_height = '0'
af_pos = '0'
gimbal_port = '0'
oriented_camera_type = '67'
oriented_file_path = '0c6f31bb-81bc-452d-904f-f15c5b92e330'
oriented_file_md5 = ''
oriented_file_size = '0'
oriented_file_suffix = 'Waypoint1'
oriented_photo_mode = 'normalPhoto'
action_actuator_func2 = 'rotateYaw'
aircraft_heading2 = '-51'
aircraft_path_mode = 'counterClockwise'
is_risky = '0'

# Add new Placemark elements for each coordinate
for idx, (lon, lat) in enumerate(coordinates):
    placemark = ET.Element(f'{{{namespaces["kml"]}}}Placemark')

    point = ET.SubElement(placemark, f'{{{namespaces["kml"]}}}Point')
    coordinates_element = ET.SubElement(
        point, f'{{{namespaces["kml"]}}}coordinates')
    coordinates_element.text = f'{lon},{lat}'

    wpml_index = ET.SubElement(placemark, f'{{{namespaces["wpml"]}}}index')
    wpml_index.text = str(idx)

    wpml_ellipsoidHeight = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}ellipsoidHeight')
    wpml_ellipsoidHeight.text = ellipsoid_height

    wpml_height = ET.SubElement(placemark, f'{{{namespaces["wpml"]}}}height')
    wpml_height.text = height

    wpml_waypointSpeed = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}waypointSpeed')
    wpml_waypointSpeed.text = waypoint_speed

    wpml_waypointHeadingParam = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}waypointHeadingParam')
    wpml_waypointHeadingMode = ET.SubElement(
        wpml_waypointHeadingParam, f'{{{namespaces["wpml"]}}}waypointHeadingMode')
    wpml_waypointHeadingMode.text = waypoint_heading_mode
    wpml_waypointHeadingAngle = ET.SubElement(
        wpml_waypointHeadingParam, f'{{{namespaces["wpml"]}}}waypointHeadingAngle')
    wpml_waypointHeadingAngle.text = waypoint_heading_angle
    wpml_waypointPoiPoint = ET.SubElement(
        wpml_waypointHeadingParam, f'{{{namespaces["wpml"]}}}waypointPoiPoint')
    wpml_waypointPoiPoint.text = waypoint_poi_point
    wpml_waypointHeadingPathMode = ET.SubElement(
        wpml_waypointHeadingParam, f'{{{namespaces["wpml"]}}}waypointHeadingPathMode')
    wpml_waypointHeadingPathMode.text = waypoint_heading_path_mode
    wpml_waypointHeadingPoiIndex = ET.SubElement(
        wpml_waypointHeadingParam, f'{{{namespaces["wpml"]}}}waypointHeadingPoiIndex')
    wpml_waypointHeadingPoiIndex.text = waypoint_heading_poi_index

    wpml_useGlobalTurnParam = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}useGlobalTurnParam')
    wpml_useGlobalTurnParam.text = use_global_turn_param

    wpml_useStraightLine = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}useStraightLine')
    wpml_useStraightLine.text = use_straight_line

    wpml_actionGroup = ET.SubElement(
        placemark, f'{{{namespaces["wpml"]}}}actionGroup')
    wpml_actionGroupId = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}actionGroupId')
    wpml_actionGroupId.text = action_group_id
    wpml_actionGroupStartIndex = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}actionGroupStartIndex')
    wpml_actionGroupStartIndex.text = action_group_start_index
    wpml_actionGroupEndIndex = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}actionGroupEndIndex')
    wpml_actionGroupEndIndex.text = action_group_end_index
    wpml_actionGroupMode = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}actionGroupMode')
    wpml_actionGroupMode.text = action_group_mode

    wpml_actionTrigger = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}actionTrigger')
    wpml_actionTriggerType = ET.SubElement(
        wpml_actionTrigger, f'{{{namespaces["wpml"]}}}actionTriggerType')
    wpml_actionTriggerType.text = action_trigger_type

    wpml_action = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}action')
    wpml_actionId = ET.SubElement(
        wpml_action, f'{{{namespaces["wpml"]}}}actionId')
    wpml_actionId.text = action_id
    wpml_actionActuatorFunc = ET.SubElement(
        wpml_action, f'{{{namespaces["wpml"]}}}actionActuatorFunc')
    wpml_actionActuatorFunc.text = action_actuator_func

    wpml_actionActuatorFuncParam = ET.SubElement(
        wpml_action, f'{{{namespaces["wpml"]}}}actionActuatorFuncParam')
    wpml_gimbalPitchRotateAngle = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}gimbalPitchRotateAngle')
    wpml_gimbalPitchRotateAngle.text = gimbal_pitch_rotate_angle
    wpml_gimbalRollRotateAngle = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}gimbalRollRotateAngle')
    wpml_gimbalRollRotateAngle.text = gimbal_roll_rotate_angle
    wpml_gimbalYawRotateAngle = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}gimbalYawRotateAngle')
    wpml_gimbalYawRotateAngle.text = gimbal_yaw_rotate_angle
    wpml_focusX = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}focusX')
    wpml_focusX.text = focus_x
    wpml_focusY = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}focusY')
    wpml_focusY.text = focus_y
    wpml_focusRegionWidth = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}focusRegionWidth')
    wpml_focusRegionWidth.text = focus_region_width
    wpml_focusRegionHeight = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}focusRegionHeight')
    wpml_focusRegionHeight.text = focus_region_height
    wpml_focalLength = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}focalLength')
    wpml_focalLength.text = focal_length
    wpml_aircraftHeading = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}aircraftHeading')
    wpml_aircraftHeading.text = aircraft_heading
    wpml_accurateFrameValid = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}accurateFrameValid')
    wpml_accurateFrameValid.text = accurate_frame_valid
    wpml_payloadPositionIndex = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}payloadPositionIndex')
    wpml_payloadPositionIndex.text = payload_position_index
    wpml_useGlobalPayloadLensIndex = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}useGlobalPayloadLensIndex')
    wpml_useGlobalPayloadLensIndex.text = use_global_payload_lens_index
    wpml_targetAngle = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}targetAngle')
    wpml_targetAngle.text = target_angle
    wpml_actionUUID = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}actionUUID')
    wpml_actionUUID.text = action_uuid
    wpml_imageWidth = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}imageWidth')
    wpml_imageWidth.text = image_width
    wpml_imageHeight = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}imageHeight')
    wpml_imageHeight.text = image_height
    wpml_AFPos = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}AFPos')
    wpml_AFPos.text = af_pos
    wpml_gimbalPort = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}gimbalPort')
    wpml_gimbalPort.text = gimbal_port
    wpml_orientedCameraType = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedCameraType')
    wpml_orientedCameraType.text = oriented_camera_type
    wpml_orientedFilePath = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedFilePath')
    wpml_orientedFilePath.text = oriented_file_path
    wpml_orientedFileMD5 = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedFileMD5')
    wpml_orientedFileSize = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedFileSize')
    wpml_orientedFileSize.text = oriented_file_size
    wpml_orientedFileSuffix = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedFileSuffix')
    wpml_orientedFileSuffix.text = oriented_file_suffix
    wpml_orientedPhotoMode = ET.SubElement(
        wpml_actionActuatorFuncParam, f'{{{namespaces["wpml"]}}}orientedPhotoMode')
    wpml_orientedPhotoMode.text = oriented_photo_mode

    wpml_action2 = ET.SubElement(
        wpml_actionGroup, f'{{{namespaces["wpml"]}}}action')
    wpml_actionId2 = ET.SubElement(
        wpml_action2, f'{{{namespaces["wpml"]}}}actionId')
    wpml_actionId2.text = action_id
    wpml_actionActuatorFunc2 = ET.SubElement(
        wpml_action2, f'{{{namespaces["wpml"]}}}actionActuatorFunc')
    wpml_actionActuatorFunc2.text = action_actuator_func2

    wpml_actionActuatorFuncParam2 = ET.SubElement(
        wpml_action2, f'{{{namespaces["wpml"]}}}actionActuatorFuncParam')
    wpml_aircraftHeading2 = ET.SubElement(
        wpml_actionActuatorFuncParam2, f'{{{namespaces["wpml"]}}}aircraftHeading')
    wpml_aircraftHeading2.text = aircraft_heading2
    wpml_aircraftPathMode = ET.SubElement(
        wpml_actionActuatorFuncParam2, f'{{{namespaces["wpml"]}}}aircraftPathMode')
    wpml_aircraftPathMode.text = aircraft_path_mode

    wpml_isRisky = ET.SubElement(placemark, f'{{{namespaces["wpml"]}}}isRisky')
    wpml_isRisky.text = is_risky

    folder.append(placemark)

# Write the updated KML to a new file
os.makedirs(os.path.dirname(output_kml_file_path), exist_ok=True)
tree.write(output_kml_file_path, encoding='UTF-8', xml_declaration=True)
