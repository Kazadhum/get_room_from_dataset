import open3d as o3d
import numpy as np

def crop_mesh_by_bb(mesh_path, output_path, bb_min, bb_max):
    original_mesh = o3d.io.read_triangle_mesh(mesh_path)

    # o3d.visualization.draw_geometries([original_mesh])

def main():
    original_mesh_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/matterport_mesh/7812e14df5e746388ff6cfe8b043950a/7812e14df5e746388ff6cfe8b043950a.obj'

    region_mesh_path = '/home/diogo/Desktop/mp3d_dataset/2azQ1b91cZZ/v1/scans/2azQ1b91cZZ/2azQ1b91cZZ/region_segmentations/region18.ply'

    unpolished_region_mesh = o3d.io.read_triangle_mesh(region_mesh_path)

    region_point_cloud = o3d.geometry.PointCloud()
    region_point_cloud.points = unpolished_region_mesh.vertices

    region_bb = region_point_cloud.get_oriented_bounding_box()

    region_mesh_oriented = unpolished_region_mesh.rotate(region_bb.R)

    original_mesh = o3d.io.read_triangle_mesh(original_mesh_path)
    original_mesh_oriented = original_mesh.rotate(region_bb.R)

    o3d.visualization.draw_geometries([original_mesh_oriented, region_bb])

    # crop_mesh_by_bb(original_mesh_path, 0, 0, 0)

if __name__ == '__main__':
    main()