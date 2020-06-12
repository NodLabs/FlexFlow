cmake_minimum_required(VERSION 3.10)
project(FlexFlow)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_LIST_DIR}/cmake)
include(protobuf)
include(legion)
include(FindProtobuf)
set(FLOW_ROOT ${CMAKE_CURRENT_LIST_DIR})
protobuf_generate_cpp(FLOW_PB_SRC FLOW_PB_HDR ${FLOW_ROOT}/src/runtime/strategy.proto)
get_filename_component(FLOW_PB_INC_DIR ${FLOW_PB_HDR} DIRECTORY)
set(FLOW_INCLUDE
  ${FLOW_ROOT}/include
  ${FLOW_PB_INC_DIR}
  ${FLOW_ROOT}/
  /usr/local/cuda/include/
)
set(FLOW_SRC
  ${FLOW_PB_SRC}
  ${FLOW_ROOT}/src/mapper/mapper.cc
  ${FLOW_ROOT}/src/ops/embedding.cc
  ${FLOW_ROOT}/src/runtime/initializer.cc
  ${FLOW_ROOT}/src/runtime/model.cc
  ${FLOW_ROOT}/src/runtime/optimizer.cc
  ${FLOW_ROOT}/src/runtime/strategy.cc
)
set(FLOW_GPU_SRC
  ${FLOW_ROOT}/src/ops/batch_norm.cu
  ${FLOW_ROOT}/src/ops/concat.cu
  ${FLOW_ROOT}/src/ops/conv_2d.cu
  ${FLOW_ROOT}/src/ops/embedding.cu
  ${FLOW_ROOT}/src/ops/flat.cu
  ${FLOW_ROOT}/src/ops/linear.cu
  ${FLOW_ROOT}/src/ops/mse_loss.cu
  ${FLOW_ROOT}/src/ops/pool_2d.cu
  ${FLOW_ROOT}/src/ops/softmax.cu
  ${FLOW_ROOT}/src/runtime/accessor_kernel.cu
  ${FLOW_ROOT}/src/runtime/cuda_helper.cu
  ${FLOW_ROOT}/src/runtime/initializer_kernel.cu
  ${FLOW_ROOT}/src/runtime/model.cu
  ${FLOW_ROOT}/src/runtime/optimizer_kernel.cu
)
set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS} -Wno-deprecated-gpu-targets)
cuda_add_library(flexflow ${FLOW_GPU_SRC} ${FLOW_SRC})
target_include_directories(flexflow PUBLIC ${FLOW_INCLUDE})

set(protobuf_lib_name protobuf)
if(CMAKE_BUILD_TYPE MATCHES "Debug")
  set(protobuf_lib_name protobufd)
endif()
target_link_libraries(flexflow Legion::Legion ${protobuf_lib_name} cudnn cublas curand "-L /usr/local/cuda/lib64")

function(link_flexflow_deps target_name)
  if(CMAKE_BUILD_TYPE MATCHES "Debug")
    target_link_libraries(${target_name} Legion::Legion protobufd cudnn cublas curand "-L /usr/local/cuda/lib64")
    MESSAGE("DEBUG ENABLED")
  else()
    target_link_libraries(${target_name} Legion::Legion protobuf cudnn cublas curand "-L /usr/local/cuda/lib64")
  endif()
endfunction()


option(BUILD_RESNET "build resnet example" OFF)
option(BUILD_ALEXNET "build alexnet example" OFF)
option(BUILD_ALEXNET_NEWAPI "build alexnet_newapi example" OFF)
option(BUILD_INCEPTION "build inception example" OFF)


if(${BUILD_RESNET})
  add_subdirectory(examples/resnet)
endif()

if(${BUILD_ALEXNET})
  add_subdirectory(examples/AlexNet)
endif()

if(${BUILD_ALEXNET_NEWAPI})
  add_subdirectory(examples/AlexNet_newapi)
endif()

if(${BUILD_INCEPTION})
  add_subdirectory(examples/InceptionV3)
endif()

