# This is a derivative work of the unlicensed repository https://github.com/cube-c/Auto-Align

import bpy
import numpy as np
from enum import Enum, auto

DEFAULT_ITERATION_RANSAC = 200
DEFAULT_ITERATION_MEDIAN = 10
DEFAULT_THRESHOLD = 5 * (np.pi / 180)
DEFAULT_MAX_POLYS = 10000

class AlignMode(Enum):
    ORIGIN_TO_OBJECT = auto()
    OBJECT_TO_ORIGIN = auto()

def align(context, align_mode: AlignMode):
    keep_bucket = []  
    
    for obj in context.selected_objects:
        if obj.type != "MESH":
            continue

        polys = obj.data.polygons
        if len(polys) == 0:
            continue
        
        matrix_basis_np = np.array(obj.matrix_basis)
        areas = np.array([p.area for p in polys])
        normals = np.array([list(p.normal) for p in polys]) @ matrix_basis_np[:3, :3].T
        normals = normals / np.linalg.norm(normals, axis=1).reshape(-1, 1)
        mesh_matrix = get_matrix(areas, normals)
        matrix_basis_np[:3, :3] = mesh_matrix @ matrix_basis_np[:3, :3]

        obj.matrix_basis = matrix_basis_np.T

        if align_mode == AlignMode.ORIGIN_TO_OBJECT:
            keep_bucket.append((obj, mesh_matrix))

    if align_mode == AlignMode.ORIGIN_TO_OBJECT:
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        for obj, mesh_matrix in keep_bucket:
            matrix_basis_np = np.array(obj.matrix_basis)
            matrix_basis_np[:3, :3] = mesh_matrix.T @ matrix_basis_np[:3, :3]
            
            obj.matrix_basis = matrix_basis_np.T

    if align_mode == AlignMode.OBJECT_TO_ORIGIN:
        pass  # TODO: Implementation for reverse transformation.

def get_matrix(areas, normals, fixed_axis=None):
    if areas.size > DEFAULT_MAX_POLYS:
        indices = np.random.choice(areas.size, DEFAULT_MAX_POLYS, p=areas/sum(areas), replace=False)
        areas = areas[indices]
        normals = normals[indices]

    first_indices = np.random.choice(areas.size, DEFAULT_ITERATION_RANSAC, p=areas/sum(areas))

    best_model = np.identity(3)
    best_value = -1.0
    best_indices = None

    for index in first_indices:
        model = np.zeros((3, 3))

        if fixed_axis is None:
            model[0] = normals[index]
        else:
            model[0] = fixed_axis
        
        next_indices = np.nonzero(np.abs(normals@model[0]) < np.sin(DEFAULT_THRESHOLD))[0]

        if next_indices.size > 0:
            next_areas = areas[next_indices]
            model[1] = normals[np.random.choice(next_indices, p=next_areas/sum(next_areas))]
        else:
            model[1] = np.zeros(3)
            model[1][(np.argmax(np.abs(model[0]))+1) % 3] = 1

        model[1] = np.cross(model[0], model[1])
        model[1] = model[1] / np.linalg.norm(model[1])
        model[2] = np.cross(model[0], model[1])

        indices = np.max(np.abs(normals@model.T), axis=1) > np.cos(DEFAULT_THRESHOLD)
        
        value = np.sum(areas[indices])
        if best_value < value:
            best_value, best_model, best_indices = value, model, indices

    areas = areas[best_indices]
    normals = normals[best_indices]
    
    axis = np.vstack((best_model, -best_model))
    axis_indices = np.argmax(normals@axis.T, axis=1)
    
    normals_per_axis = []
    areas_per_axis = []
    xyz_axis = np.array([[[1, 2], [2, 4], [4, 5], [5, 1]], [[3, 2], [2, 0], [0, 5], [5, 3]], [[0, 1], [1, 3], [3, 4], [4, 0]]])
    for i in range(6):
        normals_per_axis.append(normals[axis_indices == i])
        areas_per_axis.append(areas[axis_indices == i])

    normals_area = []
    for i in range(3):
        normals_area.append(np.concatenate([areas_per_axis[a] for (a, _) in xyz_axis[i]]))

    for _ in range(DEFAULT_ITERATION_MEDIAN):
        for i in range(3):
            if fixed_axis is not None and i != 0:
                continue

            normals_proj = np.concatenate([normals_per_axis[a] @ axis[b] for (a, b) in xyz_axis[i]])

            if normals_proj.size == 0:
                continue

            sort_indices = np.argsort(normals_proj)
            value = normals_proj[sort_indices]
            weight = normals_area[i][sort_indices]
            weight_cumsum = np.cumsum(weight)
            med_index = np.searchsorted(weight_cumsum, weight_cumsum[-1]/2)

            c, s = np.cos(value[med_index]), np.sin(value[med_index])
            j, k = (i+1) % 3, (i+2) % 3
            transform = np.identity(3)
            transform[(j, j, k, k), (j, k, j, k)] = np.array([c, -s, s, c])
            
            best_model = transform.T @ best_model
            axis = np.vstack((best_model, -best_model))

    unit_rot = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    flip_rot = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    unit_diag = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])

    best_model_opt = best_model
    best_trace = 0
    rot = np.identity(3)
    
    for _ in range(3):
        rot = unit_rot @ rot
        for j in range(4):
            model_opt = np.diag(unit_diag[j]) @ rot @ best_model
            trace = np.trace(model_opt)
            if trace > best_trace:
                best_trace, best_model_opt = trace, model_opt

            model_opt = -np.diag(unit_diag[j]) @ flip_rot @ rot @ best_model
            trace = np.trace(model_opt)
            if trace > best_trace:
                best_trace, best_model_opt = trace, model_opt

    return best_model_opt
