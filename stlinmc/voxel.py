"""
# voxel.py
# this module creates a voxel array from an stl
"""

from stl import mesh
from stltovoxel import convert_meshes
import numpy as np


def import_stl_as_voxels(input_file_path, parallel):
    """imports an stl file into a voxel array

    Args:
        input_file_path (str): path to stl file

    Returns:
        np.nDArray[int8]: a set of voxels in a 3D array,
                          0 and 1 indicate air and block respectively
    """
    meshes = []
    mesh_obj = mesh.Mesh.from_file(input_file_path)
    org_mesh = np.hstack(
        (mesh_obj.v0[:, np.newaxis], mesh_obj.v1[:, np.newaxis], mesh_obj.v2[:, np.newaxis]))
    meshes.append(org_mesh)
    vol = convert_meshes(meshes, resolution=100, parallel=parallel)[0]
    return vol
