package com.example.mathengine;

import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Pointer;

public class MathEngine {
    
    // JNA interface for C++ library
    public interface MathEngineLib extends Library {
        MathEngineLib INSTANCE = Native.load("mathengine", MathEngineLib.class);
        
        Pointer matrix_create(long rows, long cols);
        void matrix_destroy(Pointer matrix);
        void matrix_set_data(Pointer matrix, double[] data);
        void matrix_get_data(Pointer matrix, double[] data);
        Pointer matrix_multiply(Pointer a, Pointer b);
        Pointer matrix_add(Pointer a, Pointer b);
        Pointer matrix_transpose(Pointer matrix);
        long matrix_rows(Pointer matrix);
        long matrix_cols(Pointer matrix);
    }
    
    public static class Matrix implements AutoCloseable {
        private Pointer nativeMatrix;
        private final long rows;
        private final long cols;
        
        public Matrix(long rows, long cols) {
            this.rows = rows;
            this.cols = cols;
            this.nativeMatrix = MathEngineLib.INSTANCE.matrix_create(rows, cols);
            if (nativeMatrix == null) {
                throw new RuntimeException("Failed to create matrix");
            }
        }
        
        public Matrix(long rows, long cols, double[] data) {
            this(rows, cols);
            setData(data);
        }
        
        private Matrix(Pointer nativeMatrix) {
            this.nativeMatrix = nativeMatrix;
            this.rows = MathEngineLib.INSTANCE.matrix_rows(nativeMatrix);
            this.cols = MathEngineLib.INSTANCE.matrix_cols(nativeMatrix);
        }
        
        public void setData(double[] data) {
            if (data.length != rows * cols) {
                throw new IllegalArgumentException("Data size does not match matrix dimensions");
            }
            MathEngineLib.INSTANCE.matrix_set_data(nativeMatrix, data);
        }
        
        public double[] getData() {
            double[] data = new double[(int)(rows * cols)];
            MathEngineLib.INSTANCE.matrix_get_data(nativeMatrix, data);
            return data;
        }
        
        public Matrix multiply(Matrix other) {
            Pointer result = MathEngineLib.INSTANCE.matrix_multiply(nativeMatrix, other.nativeMatrix);
            if (result == null) {
                throw new RuntimeException("Matrix multiplication failed");
            }
            return new Matrix(result);
        }
        
        public Matrix add(Matrix other) {
            Pointer result = MathEngineLib.INSTANCE.matrix_add(nativeMatrix, other.nativeMatrix);
            if (result == null) {
                throw new RuntimeException("Matrix addition failed");
            }
            return new Matrix(result);
        }
        
        public Matrix transpose() {
            Pointer result = MathEngineLib.INSTANCE.matrix_transpose(nativeMatrix);
            if (result == null) {
                throw new RuntimeException("Matrix transpose failed");
            }
            return new Matrix(result);
        }
        
        public long getRows() { return rows; }
        public long getCols() { return cols; }
        
        @Override
        public void close() {
            if (nativeMatrix != null) {
                MathEngineLib.INSTANCE.matrix_destroy(nativeMatrix);
                nativeMatrix = null;
            }
        }
    }
    
    public static void main(String[] args) {
        // Example usage
        try (Matrix a = new Matrix(2, 3, new double[]{1, 2, 3, 4, 5, 6});
             Matrix b = new Matrix(3, 2, new double[]{7, 8, 9, 10, 11, 12})) {
            
            Matrix c = a.multiply(b);
            double[] result = c.getData();
            
            System.out.println("Matrix multiplication result:");
            for (int i = 0; i < c.getRows(); i++) {
                for (int j = 0; j < c.getCols(); j++) {
                    System.out.printf("%.0f ", result[(int)(i * c.getCols() + j)]);
                }
                System.out.println();
            }
            c.close();
        }
    }
}