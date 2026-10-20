cmake_minimum_required(VERSION 3.20)
project(workbook LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Debug)
endif()

# In Debug, std::vector::operator[] and friends are bounds-checked, so an
# off-by-one stops with a clear message instead of printing wrong numbers.
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wno-unused-parameter $<$<CONFIG:Debug>:-D_GLIBCXX_ASSERTIONS>)
endif()
if(MINGW)
  add_link_options(-static)  # no runtime DLLs needed to run the programs
endif()
include_directories(include)  # add third_party/<library> folders here

# Code the learner shares between checkpoints: every .cpp in solutions/common/ is compiled
# once and linked into each learner program (not the reference ones). Headers are included
# as "common/name.h". New files are picked up on the next build.
file(GLOB COMMON_SOURCES CONFIGURE_DEPENDS ${CMAKE_SOURCE_DIR}/solutions/common/*.cpp)
if(COMMON_SOURCES)
  add_library(common OBJECT ${COMMON_SOURCES})
  target_include_directories(common PUBLIC solutions)
endif()

# One program per checkpoint: p<id> is the learner's, ref_p<id> the reference (spoiler).
# A program is only added once its source file exists; the checker re-runs this
# configuration step when it meets a new one.
function(add_checkpoint id slug)
  if(EXISTS ${CMAKE_SOURCE_DIR}/solutions/p${id}_${slug}.cpp)
    add_executable(p${id} solutions/p${id}_${slug}.cpp)
    target_include_directories(p${id} PRIVATE solutions)
    if(TARGET common)
      target_link_libraries(p${id} PRIVATE common)
    endif()
  endif()
  if(EXISTS ${CMAKE_SOURCE_DIR}/_spoilers/reference/p${id}_${slug}.cpp)
    add_executable(ref_p${id} _spoilers/reference/p${id}_${slug}.cpp)
  endif()
endfunction()

# add_checkpoint(01 first_slug)
