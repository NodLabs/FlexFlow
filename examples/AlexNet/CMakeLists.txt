cmake_minimum_required(VERSION 3.1)

project(FlexFlowExample_AlexNet)
set(project_target alexnet)

set(CPU_SOURCES
  ${FLOW_SRC}
  alexnet.cc
  alexnet.cu
  alexnet.h)

set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS} -Wno-deprecated-gpu-targets)
set(GPU_SOURCES ${FLOW_GPU_SRCS})

cuda_add_executable(${project_target} ${CPU_SOURCES} ${FLOW_GPU_SRC})
target_include_directories(${project_target} PRIVATE ${FLOW_INCLUDE} ${CMAKE_INSTALL_INCLUDEDIR})
link_flexflow_deps(${project_target})
add_dependencies(${project_target} ${NODPROTOC})
