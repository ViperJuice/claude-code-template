#include "math_engine.h"

// C API implementation
extern "C" {

void* matrix_create(size_t rows, size_t cols) {
    try {
        return new math_engine::Matrix(rows, cols);
    } catch (...) {
        return nullptr;
    }
}

void matrix_destroy(void* matrix) {
    delete static_cast<math_engine::Matrix*>(matrix);
}

void matrix_set_data(void* matrix, const double* data) {
    auto* m = static_cast<math_engine::Matrix*>(matrix);
    std::copy(data, data + (m->rows() * m->cols()), m->data());
}

void matrix_get_data(void* matrix, double* data) {
    auto* m = static_cast<math_engine::Matrix*>(matrix);
    std::copy(m->data(), m->data() + (m->rows() * m->cols()), data);
}

void* matrix_multiply(void* a, void* b) {
    try {
        auto* ma = static_cast<math_engine::Matrix*>(a);
        auto* mb = static_cast<math_engine::Matrix*>(b);
        auto result = *ma * *mb;
        return new math_engine::Matrix(std::move(result));
    } catch (...) {
        return nullptr;
    }
}

void* matrix_add(void* a, void* b) {
    try {
        auto* ma = static_cast<math_engine::Matrix*>(a);
        auto* mb = static_cast<math_engine::Matrix*>(b);
        auto result = *ma + *mb;
        return new math_engine::Matrix(std::move(result));
    } catch (...) {
        return nullptr;
    }
}

void* matrix_transpose(void* matrix) {
    try {
        auto* m = static_cast<math_engine::Matrix*>(matrix);
        auto result = m->transpose();
        return new math_engine::Matrix(std::move(result));
    } catch (...) {
        return nullptr;
    }
}

size_t matrix_rows(void* matrix) {
    auto* m = static_cast<math_engine::Matrix*>(matrix);
    return m->rows();
}

size_t matrix_cols(void* matrix) {
    auto* m = static_cast<math_engine::Matrix*>(matrix);
    return m->cols();
}

} // extern "C"