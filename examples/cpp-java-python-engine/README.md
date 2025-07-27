# C++ Engine with Java Wrapper and Python Bindings

This example demonstrates building a high-performance C++ calculation engine with Java enterprise wrapper and Python data science bindings.

## Architecture

```
                    ┌─────────────────┐
                    │   C++ Engine    │
                    │  (Core Logic)   │
                    └────────┬────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐       ┌───────▼────────┐
        │  Java Wrapper  │       │Python Bindings │
        │  (Enterprise)  │       │(Data Science)  │
        └────────────────┘       └────────────────┘
```

## Components

### C++ Engine
- High-performance mathematical computations
- Matrix operations
- Statistical calculations
- Memory-efficient algorithms

### Java Wrapper
- Enterprise API
- Spring Boot integration ready
- Thread-safe operations
- JNI bindings

### Python Bindings
- NumPy-compatible interface
- Pandas integration
- Jupyter notebook support
- Cython optimizations

## Building

```bash
# Build everything
make all

# Build individual components
make engine
make java-wrapper
make python-bindings
```

## Usage Examples

### C++ Direct Usage
```cpp
#include "math_engine.h"

MatrixEngine engine;
auto result = engine.multiply(matrixA, matrixB);
```

### Java Usage
```java
import com.example.MathEngine;

MathEngine engine = new MathEngine();
Matrix result = engine.multiply(matrixA, matrixB);
```

### Python Usage
```python
import math_engine as me

engine = me.MathEngine()
result = engine.multiply(matrix_a, matrix_b)
```

## Performance

- C++ engine: ~100x faster than pure Python
- Java wrapper: ~2x overhead vs direct C++
- Python bindings: ~5x overhead vs direct C++

## Testing

```bash
# Run all tests
make test

# Run performance benchmarks
make benchmark
```