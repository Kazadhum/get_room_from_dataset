import os
from PIL import Image
import shutil

def rename_dataset_files(rgb_images_path, output_path, poses_path):
    """Given the images and poses in a sub-dataset acquired from Matterport, turn it into a Synfeal-compatible dataset (frame-xxxxx.rgb.png and frame-xxxxx.pose.txt in the same folder)"""

    # Get the list of rgb image file names
    rgb_image_name_list = os.listdir(rgb_images_path)
    
    # Get the list of pose file names
    pose_name_list = os.listdir(poses_path)

    image_counter = 0
    # Iterate through the list of images
    for image_name in rgb_image_name_list:

        new_image_name = 'frame-' + str(image_counter).zfill(5) + '.rgb.png'

        input_image_path = rgb_images_path + '/' + image_name
        output_image_path = output_path +  '/' + new_image_name

        # Find corresponding pose file
        image_name_parts = image_name.split('_')
        image_name_parts[1] = image_name_parts[1].replace('i', '')
        image_name_parts[2] = image_name_parts[2].replace('.jpg', '')

        if image_name_parts[1] == '0':

            # Save a new image as .rgb.png in the final dataset folder
            try:
            # Open the JPEG image
                with Image.open(input_image_path) as img:
                    # Save the image in PNG format
                    img.save(output_image_path, "PNG")
                    print(f"Conversion successful: {input_image_path} -> {output_path}")
            except Exception as e:
                print(f"Error converting image: {e}")


            # print(image_name_parts)
            
            corresponding_pose_name = image_name_parts[0] + '_pose_' + image_name_parts[1] + '_' + image_name_parts[2] + '.txt'
            # print(corresponding_pose_name) # DEBUG

            # Find the corresponding pose file
            try:
                index = pose_name_list.index(corresponding_pose_name)
                # print(f"The element {corresponding_pose_name} is at index {index}")
            except ValueError:
                print(f"The element {corresponding_pose_name} is not in the list")
            
            new_pose_name = 'frame-' + str(image_counter).zfill(5) + '.pose.txt'
            
            shutil.copy(poses_path + '/' + corresponding_pose_name, output_path + '/' + new_pose_name)

            # Change the pose file to the format of a synfeal dataset
            with open(output_path + '/' + new_pose_name, 'r') as file:
                file_content = file.read()

            altered_file_content = file_content.replace(' ', ',').replace(',\n', '\n')
        
            with open(output_path + '/' + new_pose_name, 'w') as file:
                file.write(altered_file_content)

            image_counter += 1

def main():
    
    rgb_images_path = '/home/diogo/Desktop/sub_mp3d_dataset/color_images'
    poses_path = '/home/diogo/Desktop/sub_mp3d_dataset/camera_poses'
    output_path = '/home/diogo/Desktop/sub_mp3d_dataset/test_dataset'
    rename_dataset_files(rgb_images_path, output_path, poses_path)

if __name__ == '__main__':
    main()