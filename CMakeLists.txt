cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

project(dacsim)
find_package(Python REQUIRED)
include(UseCython)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    )

configure_file(dat/scintillator.dat ${CMAKE_BINARY_DIR}/dat/scintillator.dat)
configure_file(dat/spectrum.dat ${CMAKE_BINARY_DIR}/dat/spectrum.dat)
add_subdirectory(src)