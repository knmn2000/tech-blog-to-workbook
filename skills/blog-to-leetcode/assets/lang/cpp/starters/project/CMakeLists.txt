cmake_minimum_required(VERSION 3.20)
project({{NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()

# Debug builds bounds-check std::vector and friends, so an off-by-one stops with a
# clear message instead of quietly producing wrong numbers.
add_compile_options(-Wall -Wextra -Wno-unused-parameter
                    $<$<CONFIG:Debug>:-D_GLIBCXX_ASSERTIONS>)
if(MINGW)
  add_link_options(-static)  # the programs run without the compiler's DLLs
endif()

# The project: every .cpp under src/ except main.cpp. Headers are included from src/,
# e.g. #include "parser/Reader.h", and from third_party/ (headers the workbook provides).
# New files are picked up on the next build.
file(GLOB_RECURSE CORE_SOURCES CONFIGURE_DEPENDS ${CMAKE_SOURCE_DIR}/src/*.cpp)
list(REMOVE_ITEM CORE_SOURCES ${CMAKE_SOURCE_DIR}/src/main.cpp)
if(CORE_SOURCES)
  add_library({{NAME}}_core STATIC ${CORE_SOURCES})
  target_include_directories({{NAME}}_core PUBLIC src third_party)
else()
  add_library({{NAME}}_core INTERFACE)  # only headers so far
  target_include_directories({{NAME}}_core INTERFACE src third_party)
endif()

# The finished program (the last checkpoint writes src/main.cpp).
if(EXISTS ${CMAKE_SOURCE_DIR}/src/main.cpp)
  add_executable({{NAME}} src/main.cpp)
  target_link_libraries({{NAME}} PRIVATE {{NAME}}_core)
endif()

# One small program per checkpoint (checkpoints/p03_parse_header.cpp -> p03). Each reads
# a test input, calls the project and writes what it found; the workbook's checker runs them.
file(GLOB CHECKPOINT_SOURCES CONFIGURE_DEPENDS ${CMAKE_SOURCE_DIR}/checkpoints/p*.cpp)
foreach(source ${CHECKPOINT_SOURCES})
  get_filename_component(name ${source} NAME_WE)
  string(REGEX MATCH "^p[0-9]+" target ${name})
  add_executable(${target} ${source})
  target_link_libraries(${target} PRIVATE {{NAME}}_core)
endforeach()
