set(protobuf_BUILD_TESTS OFF CACHE BOOL "Disable tests for protobuf")

set(BUILD_SHARED_LIBS OFF)
set(LIBRARY_POLICY STATIC)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../protobuf/cmake ${CMAKE_CURRENT_BINARY_DIR}/protobuf)
include_directories(${CMAKE_CURRENT_LIST_DIR}/../protobuf/src)
link_directories(${CMAKE_CURRENT_BINARY_DIR}/protobuf)
