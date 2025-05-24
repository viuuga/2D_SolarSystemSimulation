import numpy as np

def find_ellipse_center(points):
    """
    Находит центр эллипса по пяти точкам.
    Исправленная версия, которая правильно работает с симметричными эллипсами.
    """
    if len(points) != 5:
        raise ValueError("Требуется ровно 5 точек для определения эллипса.")
    
    # Преобразуем точки в numpy array
    points = np.array(points, dtype=np.float64)
    x = points[:, 0]
    y = points[:, 1]
    

    A_matrix = np.column_stack((
        x**2,
        x*y,
        y**2,
        x,
        y,
        np.ones(5)
    ))
    
    _, _, V = np.linalg.svd(A_matrix)
    coeffs = V[-1, :]
    
    A, B, C, D, E, F = coeffs
    
    discriminant = B**2 - 4*A*C
    if discriminant >= 0:
        raise ValueError("Точки не образуют эллипс (дискриминант >= 0)")
    

    M = np.array([
        [2*A, B],
        [B, 2*C]
    ])
    rhs = np.array([-D, -E])
    
    try:
        h, k = np.linalg.solve(M, rhs)
    except np.linalg.LinAlgError:
        h, k = np.linalg.lstsq(M, rhs, rcond=None)[0]
    
    return np.array([h, k])