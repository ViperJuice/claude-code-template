"""Python bindings for C++ Math Engine"""

import numpy as np
import ctypes
from ctypes import c_void_p, c_size_t, c_double, POINTER
import os
import platform

# Load the shared library
lib_name = "mathengine"
if platform.system() == "Windows":
    lib_name = "mathengine.dll"
elif platform.system() == "Darwin":
    lib_name = "libmathengine.dylib"
else:
    lib_name = "libmathengine.so"

# Try to find the library
lib_path = None
for path in ["../engine/build", "../engine/build/Release", "../engine/build/Debug", "."]:
    full_path = os.path.join(os.path.dirname(__file__), path, lib_name)
    if os.path.exists(full_path):
        lib_path = full_path
        break

if lib_path is None:
    raise ImportError(f"Could not find {lib_name}")

_lib = ctypes.CDLL(lib_path)

# Define C function signatures
_lib.matrix_create.argtypes = [c_size_t, c_size_t]
_lib.matrix_create.restype = c_void_p

_lib.matrix_destroy.argtypes = [c_void_p]
_lib.matrix_destroy.restype = None

_lib.matrix_set_data.argtypes = [c_void_p, POINTER(c_double)]
_lib.matrix_set_data.restype = None

_lib.matrix_get_data.argtypes = [c_void_p, POINTER(c_double)]
_lib.matrix_get_data.restype = None

_lib.matrix_multiply.argtypes = [c_void_p, c_void_p]
_lib.matrix_multiply.restype = c_void_p

_lib.matrix_add.argtypes = [c_void_p, c_void_p]
_lib.matrix_add.restype = c_void_p

_lib.matrix_transpose.argtypes = [c_void_p]
_lib.matrix_transpose.restype = c_void_p

_lib.matrix_rows.argtypes = [c_void_p]
_lib.matrix_rows.restype = c_size_t

_lib.matrix_cols.argtypes = [c_void_p]
_lib.matrix_cols.restype = c_size_t


class Matrix:
    """Python wrapper for C++ Matrix class"""
    
    def __init__(self, data=None, rows=None, cols=None):
        if isinstance(data, np.ndarray):
            if data.ndim != 2:
                raise ValueError("Input must be a 2D array")
            rows, cols = data.shape
            self._ptr = _lib.matrix_create(rows, cols)
            if not self._ptr:
                raise RuntimeError("Failed to create matrix")
            
            # Set data
            data_flat = data.flatten().astype(np.float64)
            data_ptr = data_flat.ctypes.data_as(POINTER(c_double))
            _lib.matrix_set_data(self._ptr, data_ptr)
        elif rows is not None and cols is not None:
            self._ptr = _lib.matrix_create(rows, cols)
            if not self._ptr:
                raise RuntimeError("Failed to create matrix")
        else:
            raise ValueError("Must provide either data array or dimensions")
    
    @classmethod
    def _from_ptr(cls, ptr):
        """Create Matrix from C++ pointer"""
        obj = cls.__new__(cls)
        obj._ptr = ptr
        return obj
    
    def __del__(self):
        if hasattr(self, '_ptr') and self._ptr:
            _lib.matrix_destroy(self._ptr)
    
    @property
    def shape(self):
        rows = _lib.matrix_rows(self._ptr)
        cols = _lib.matrix_cols(self._ptr)
        return (rows, cols)
    
    def to_numpy(self):
        """Convert to numpy array"""
        rows, cols = self.shape
        size = rows * cols
        data = (c_double * size)()
        _lib.matrix_get_data(self._ptr, data)
        return np.array(data).reshape(rows, cols)
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only add Matrix objects")
        result_ptr = _lib.matrix_add(self._ptr, other._ptr)
        if not result_ptr:
            raise RuntimeError("Matrix addition failed")
        return Matrix._from_ptr(result_ptr)
    
    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Can only multiply Matrix objects")
        result_ptr = _lib.matrix_multiply(self._ptr, other._ptr)
        if not result_ptr:
            raise RuntimeError("Matrix multiplication failed")
        return Matrix._from_ptr(result_ptr)
    
    def transpose(self):
        """Return transposed matrix"""
        result_ptr = _lib.matrix_transpose(self._ptr)
        if not result_ptr:
            raise RuntimeError("Matrix transpose failed")
        return Matrix._from_ptr(result_ptr)
    
    def __repr__(self):
        return f"Matrix{self.shape}:\\n{self.to_numpy()}"


class MathEngine:
    """High-level interface for math operations"""
    
    @staticmethod
    def multiply(a, b):
        """Multiply two matrices or arrays"""
        ma = Matrix(a) if not isinstance(a, Matrix) else a
        mb = Matrix(b) if not isinstance(b, Matrix) else b
        return (ma @ mb).to_numpy()
    
    @staticmethod
    def add(a, b):
        """Add two matrices or arrays"""
        ma = Matrix(a) if not isinstance(a, Matrix) else a
        mb = Matrix(b) if not isinstance(b, Matrix) else b
        return (ma + mb).to_numpy()
    
    @staticmethod
    def transpose(a):
        """Transpose a matrix or array"""
        ma = Matrix(a) if not isinstance(a, Matrix) else a
        return ma.transpose().to_numpy()


# Example usage
if __name__ == "__main__":
    # Create matrices
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([[7, 8], [9, 10], [11, 12]])
    
    # Use high-level interface
    engine = MathEngine()
    result = engine.multiply(a, b)
    print("Matrix multiplication result:")
    print(result)
    
    # Use low-level interface
    ma = Matrix(a)
    mb = Matrix(b)
    mc = ma @ mb
    print("\\nUsing operator overload:")
    print(mc.to_numpy())