import open3d as o3d
import numpy as np

def crop_mesh_by_bb(mesh_path, output_path, bb_min, bb_max):
    original_mesh = o3d.io.read_triangle_mesh(mesh_path)

    # o3d.visualization.draw_geometries([original_mesh])

def main():
    original_mesh_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_mesh/7812e14df5e746388ff6cfe8b043950a/7812e14df5e746388ff6cfe8b043950a.obj'

    region_mesh_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/region_segmentations/region18.ply'

    unpolished_region_mesh = o3d.io.read_triangle_mesh(region_mesh_path)

    o3d.visualization.draw_geometries([unpolished_region_mesh])

    crop_mesh_by_bb(original_mesh_path, 0, 0, 0)

if __name__ == '__main__':
    main()