cmake_minimum_required(VERSION 3.14)
project(MathEngine VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Source files
set(SOURCES
    src/matrix.cpp
    src/engine.cpp
)

# Create shared library
add_library(mathengine SHARED ${SOURCES})

# Include directories
target_include_directories(mathengine PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Export symbols for Windows
if(WIN32)
    set_target_properties(mathengine PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Install targets
install(TARGETS mathengine
    EXPORT MathEngineTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

# Install headers
install(DIRECTORY include/ DESTINATION include)

# Tests
enable_testing()
add_subdirectory(tests)