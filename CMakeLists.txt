# CMAKE version of Ubuntu 16.04 is 3.5.
cmake_minimum_required(VERSION 3.5)
project(cpp_client)

set(LINKLIBS)
set(COMPILE_OPTION)
set(SRC)
set(INCL)

list(APPEND SRC
  client.cpp
  )

add_executable(${PROJECT_NAME} ${SRC})

#############################################

list(APPEND INCL
  ${PROJECT_SOURCE_DIR}/curl
  )

list(APPEND COMPILE_OPTION

  #gdb debugging option
  -g
  -ggdb
  -Wextra
  -Wcast-align # warn for potential performance problem casts
  -Wno-unused-result
  -Wno-reorder
  -Wno-unused-parameter
  -Wall
  -Wfatal-errors
  )

list(APPEND LINKLIBS
    ${PROJECT_SOURCE_DIR}/curl/libcurl.so
    )

###############################################

target_include_directories(${PROJECT_NAME}	PRIVATE	${INCL} )
target_link_libraries(${PROJECT_NAME} ${LINKLIBS})
target_compile_options(${PROJECT_NAME} PRIVATE ${COMPILE_OPTION} )
set_target_properties(${PROJECT_NAME} PROPERTIES  CXX_STANDARD 14 )





