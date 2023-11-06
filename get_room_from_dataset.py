# This script is to be used to get a sub-dataset from a bigger camera localization dataset, like the Matterport3D dataset. The goal is to take a dataset corresponding to an entire house and to get a sub-dataset corresponding to a single room in that house.

from aux_funcs import *


def main():
    
    rgb_images_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_color_images'
    
    rgb_image_name_list = get_files_from_directory(rgb_images_path)

    camera_poses_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_camera_poses'

    camera_pose_name_list = get_files_from_directory(camera_poses_path)

    pose_file_name_in_room_list = filter_poses(camera_pose_name_list, camera_poses_path)
    
    res = make_sub_dataset(pose_file_name_in_room_list)


if __name__ == '__main__':
    main()
