"""Align utilities for mesh alignment.

This module provides functionality to automatically align mesh objects with
their origins and coordinate axes using RANSAC algorithm for robust estimation.

Note: This is a derivative work based on the Auto-Align repository from
https://github.com/cube-c/Auto-Align (unlicensed original).
"""

import bpy
import math
import numpy as np
from enum import Enum, auto


DEFAULT_ITERATION_RANSAC = 200
DEFAULT_ITERATION_MEDIAN = 10
DEFAULT_THRESHOLD = 5 * (math.pi / 180)
DEFAULT_MAX_POLYS = 10000


class AlignMode(Enum):
    """Alignment modes for mesh correction."""

    ORIGIN_TO_OBJECT = auto()
    OBJECT_TO_ORIGIN = auto()


def align(context: dict, align_mode: AlignMode) -> None:
    """Align selected mesh objects to their geometry or vice versa.

    Args:
        context: Blender context containing selected objects.
        align_mode: Alignment mode - either 'ORIGIN_TO_OBJECT' or 'OBJECT_TO_ORIGIN'.

    This function aligns the selected mesh objects based on their dominant axis
    using a RANSAC-based algorithm for robust estimation.
    """
    keep_bucket = []

    for obj in context.selected_objects:
        if obj.type != "MESH":
            continue

        polys = obj.data.polygons
        if len(polys) == 0:
            continue

        matrix_basis_np = np.array(obj.matrix_basis)
        areas = np.array([p.area for p in polys])
        normals = np.array(
            [list(p.normal) for p in polys]
        ) @ matrix_basis_np[:3, :3].T
        norms = np.linalg.norm(normals, axis=1).reshape(-1, 1)
        normals = normals / norms
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


def get_matrix(areas: np.ndarray, normals: np.ndarray, fixed_axis=None) -> np.ndarray:
    """Compute optimal rotation matrix using RANSAC algorithm.

    Args:
        areas: Array of polygon areas used for weighted voting.
        normals: Array of polygon normals.
        fixed_axis: Optional fixed axis to constrain the solution.

    Returns:
        Optimal 3x3 rotation matrix aligning normals to cardinal axes.
    """
    # Resample if too many polygons
    if areas.size > DEFAULT_MAX_POLYS:
        indices = np.random.choice(
            areas.size, DEFAULT_MAX_POLYS, p=areas / sum(areas), replace=False
        )
        areas = areas[indices]
        normals = normals[indices]

    first_indices = np.random.choice(
        areas.size, DEFAULT_ITERATION_RANSAC, p=areas / sum(areas)
    )

    best_model = np.identity(3)
    best_value = -1.0
    best_indices = None

    for index in first_indices:
        model = np.zeros((3, 3))

        if fixed_axis is None:
            model[0] = normals[index]
        else:
            model[0] = fixed_axis

        next_indices = np.nonzero(
            np.abs(normals @ model[0]) < np.sin(DEFAULT_THRESHOLD)
        )[0]

        if next_indices.size > 0:
            next_areas = areas[next_indices]
            model[1] = normals[np.random.choice(
                next_indices, p=next_areas / sum(next_areas)
            )]
        else:
            model[1] = np.zeros(3)
            model[1][((np.argmax(np.abs(model[0])) + 1) % 3)] = 1

        model[1] = np.cross(model[0], model[1])
        norm = np.linalg.norm(model[1])
        if norm > 0:
            model[1] = model[1] / norm
        else:
            continue

        model[2] = np.cross(model[0], model[1])

        indices = np.max(np.abs(normals @ model.T), axis=1) > np.cos(DEFAULT_THRESHOLD)

        value = np.sum(areas[indices])
        if best_value < value:
            best_value, best_model, best_indices = value, model, indices

    areas = areas[best_indices]
    normals = normals[best_indices]

    axis = np.vstack((best_model, -best_model))
    axis_indices = np.argmax(normals @ axis.T, axis=1)

    normals_per_axis = []
    areas_per_axis = []
    xyz_axis = np.array(
        [
            [[1, 2], [2, 4], [4, 5], [5, 1]],
            [[3, 2], [2, 0], [0, 5], [5, 3]],
            [[0, 1], [1, 3], [3, 4], [4, 0]]
        ]
    )

    for i in range(6):
        normals_per_axis.append(normals[axis_indices == i])
        areas_per_axis.append(areas[axis_indices == i])

    normals_area = []
    for i in range(3):
        normals_area.append(
            np.concatenate([areas_per_axis[a] for (a, _) in xyz_axis[i]])
        )

    for _ in range(DEFAULT_ITERATION_MEDIAN):
        for i in range(3):
            if fixed_axis is not None and i != 0:
                continue

            normals_proj = np.concatenate(
                [normals_per_axis[a] @ axis[b] for (a, b) in xyz_axis[i]]
            )

            if normals_proj.size == 0:
                continue

            sort_indices = np.argsort(normals_proj)
            value = normals_proj[sort_indices]
            weight = normals_area[i][sort_indices]
            weight_cumsum = np.cumsum(weight)
            med_index = np.searchsorted(
                weight_cumsum, weight_cumsum[-1] / 2
            )

            c, s = math.cos(value[med_index]), math.sin(value[med_index])
            j, k = (i + 1) % 3, (i + 2) % 3

            # Create 2x2 rotation matrix for the specified 2x2 submatrix
            rot_2x2 = np.array([[c, -s], [s, c]])
            
            transform = np.identity(3)
            transform[j, j] = rot_2x2[0, 0]
            transform[j, k] = rot_2x2[0, 1]
            transform[k, j] = rot_2x2[1, 0]
            transform[k, k] = rot_2x2[1, 1]

            best_model = transform.T @ best_model
            axis = np.vstack((best_model, -best_model))

    unit_rot = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    flip_rot = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    unit_diag = np.array(
        [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    )

    best_model_opt = best_model
    best_trace = 0
    rot = np.identity(3)

    for _ in range(3):
        rot = unit_rot @ rot
        for j in range(4):
            model_opt = (np.diag(unit_diag[j]) @ rot @ best_model)
            trace = np.trace(model_opt)
            if trace > best_trace:
                best_trace, best_model_opt = trace, model_opt

            model_opt = (-np.diag(unit_diag[j]) @ flip_rot @ rot @ best_model)
            trace = np.trace(model_opt)
            if trace > best_trace:
                best_trace, best_model_opt = trace, model_opt

    return best_model_opt