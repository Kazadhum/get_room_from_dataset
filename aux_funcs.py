import os
import math
import numpy as np
import pyvista as pv
import time
import open3d as o3d

def get_files_from_directory(path):
    """Input: a path to a directory; Output: a list of all the files in that directory"""

    file_list = os.listdir(path)
    
    return file_list


def get_pose_dict(camera_pose_name_list, camera_poses_path):
    
    """For all of the camera pose files in the dataset, reads it and turns the transform matrix into [x,y,z,R,P,Y] values. Returns a dictionary with these values for each pose file."""

    pose_dict = {}

    for pose in camera_pose_name_list:
        pose_file = open(camera_poses_path + '/' + pose, 'r')

        pose_matrix = read_pose_from_file(pose_file)

        pose_file.close()

        pose_xyzrpy = pose_matrix_to_xyzrpy(pose_matrix)

        pose_dict[pose] = pose_xyzrpy

    return pose_dict

def read_pose_from_file(file):
    
    """This functions simply reads a camera pose (as a transform matrix) from a file and returns a matrix with the values as floats."""

    str_pose = file.readlines()

    # Turn the list of strings into a 4x4 matrix

    pose_matrix = []

    for string in str_pose:
        # remove newline char
        line_list = string.replace('\n', '').strip().split(' ')
        line_list = [float(x) for x in line_list]
        pose_matrix.append(line_list)

    return pose_matrix

def pose_matrix_to_xyzrpy(pose_matrix):

    """This function receives a camera's pose as a transform matrix (from the read_pose_from_file() function) and returns the camera's pose in the form of XYZRPY values."""

    pose_matrix = np.array(pose_matrix) # Convert to np array
    x = pose_matrix[0,3]
    y = pose_matrix[1,3]
    z = pose_matrix[2,3]

    ## GET ORIENTATIONS FORM MATRIX (p.73 robotics book)

    # Check if cos(theta) == 0
    sy = math.sqrt(pose_matrix[0,0]*pose_matrix[0,0] + pose_matrix[1,0]*pose_matrix[1,0]) 

    singular = sy < 1e-6

    if not singular:
        phi = math.atan2(pose_matrix[1 ,0], pose_matrix[0,0]) # rotx
        theta = math.atan2(-pose_matrix[2,0], sy) # roty
        psi = math.atan2(pose_matrix[2,1], pose_matrix[2,2]) # rotz

    else:
        phi = 0 # rotx
        theta = math.atan2(-pose_matrix[2,0], sy) # roty
        psi = math.atan2(pose_matrix[0,1], pose_matrix[1,1])
    
    pose_xyzrpy = [x,y,z,phi,theta,psi]

    return pose_xyzrpy


def filter_poses(camera_pose_name_list, camera_poses_path):
    
    """ This function filters the different camera poses in a dictionary to see if they are inside a polyhedron. Returns a list of file names that contain those that are inside the polyhedron."""

    pose_dict = get_pose_dict(camera_pose_name_list, camera_poses_path)

    # Defining the polyhedron's vertices (using CloudCompare to get these values)
    bb_vertices = [
        [22.712818, 11.215570, 2.639785],
        [18.549446, 11.224643, 2.602052],
        [18.500113, 7.984735, 2.602463],
        [22.721617, 7.966275, 2.635593],
        [22.637238, 11.330083, -0.02316],
        [18.597948, 11.257102, -0.026202],
        [18.548159, 7.988379, -0.032970],
        [22.677464, 7.987204, -0.027993]
    ]

    # Defining the polyhedron's faces
    #poly_faces = np.array([
    #    [1,2,3,4],
    #    [5,6,7,8],
    #    [1,5,6,2],
    #    [2,6,7,3],
    #    [3,7,8,4],
    #    [4,8,5,1]
    #])

    #polyhedron = pv.PolyData(poly_vertices, poly_faces)
    bb_vertices = o3d.utility.Vector3dVector(bb_vertices)

    bb = o3d.geometry.OrientedBoundingBox.create_from_points(bb_vertices)

    list_of_poses_in_polyhedron = []

    camera_position_list = [pose_dict[pose_file_name][0:3] for pose_file_name in pose_dict]
   
    camera_position_list_vec = o3d.utility.Vector3dVector(camera_position_list)
    
    ind = bb.get_point_indices_within_bounding_box(points=camera_position_list_vec)
    
    pose_file_name_list = [pose_file_name for pose_file_name in pose_dict]
    pose_file_name_in_bb_list = [pose_file_name_list[i] for i in ind]


    return pose_file_name_in_bb_list


def make_sub_dataset(pose_file_list: list):

    import shutil
    
    source_pose_directory = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_camera_poses'

    dest_pose_directory = '/home/diogo/Desktop/sub_mp3d_dataset/camera_poses'
    
    source_color_image_directory = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_color_images'

    dest_color_image_directory = '/home/diogo/Desktop/sub_mp3d_dataset/color_images'

    region_number = 18

    source_submesh_directory = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/region_segmentations'

    dest_submesh_directory = '/home/diogo/Desktop/sub_mp3d_dataset/mesh'

    for pose_file in pose_file_list:

        # copy pose files
        source_pose_path = os.path.join(source_pose_directory, os.path.basename(pose_file))
        dest_pose_path = os.path.join(dest_pose_directory, os.path.basename(pose_file))
        shutil.copy(source_pose_path, dest_pose_path)

        # copy rgb image files
        color_image_file = pose_file.replace('.txt', '.jpg')
        color_image_file = color_image_file.replace('pose_', 'i')
        source_color_image_path = os.path.join(source_color_image_directory, os.path.basename(color_image_file))
        dest_color_image_path = os.path.join(dest_color_image_directory, os.path.basename(color_image_file))
        shutil.copy(source_color_image_path, dest_color_image_path)

    # copy sub-mesh
    source_submesh_path = os.path.join(source_submesh_directory, os.path.basename('region'+str(region_number)+'.ply'))
    dest_submesh_path = os.path.join(dest_submesh_directory, os.path.basename('region'+str(region_number)+'.ply'))
    shutil.copy(source_submesh_path, dest_submesh_path)

    return 0
