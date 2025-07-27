#ifndef MATH_ENGINE_H
#define MATH_ENGINE_H

#include <vector>
#include <stdexcept>

#ifdef _WIN32
    #ifdef MATHENGINE_EXPORTS
        #define MATHENGINE_API __declspec(dllexport)
    #else
        #define MATHENGINE_API __declspec(dllimport)
    #endif
#else
    #define MATHENGINE_API
#endif

namespace math_engine {

class MATHENGINE_API Matrix {
public:
    Matrix(size_t rows, size_t cols);
    Matrix(size_t rows, size_t cols, const std::vector<double>& data);
    
    size_t rows() const { return rows_; }
    size_t cols() const { return cols_; }
    
    double& at(size_t row, size_t col);
    const double& at(size_t row, size_t col) const;
    
    Matrix operator+(const Matrix& other) const;
    Matrix operator*(const Matrix& other) const;
    Matrix transpose() const;
    
    const double* data() const { return data_.data(); }
    double* data() { return data_.data(); }

private:
    size_t rows_;
    size_t cols_;
    std::vector<double> data_;
};

// C API for bindings
extern "C" {
    MATHENGINE_API void* matrix_create(size_t rows, size_t cols);
    MATHENGINE_API void matrix_destroy(void* matrix);
    MATHENGINE_API void matrix_set_data(void* matrix, const double* data);
    MATHENGINE_API void matrix_get_data(void* matrix, double* data);
    MATHENGINE_API void* matrix_multiply(void* a, void* b);
    MATHENGINE_API void* matrix_add(void* a, void* b);
    MATHENGINE_API void* matrix_transpose(void* matrix);
    MATHENGINE_API size_t matrix_rows(void* matrix);
    MATHENGINE_API size_t matrix_cols(void* matrix);
}

} // namespace math_engine

#endif // MATH_ENGINE_H