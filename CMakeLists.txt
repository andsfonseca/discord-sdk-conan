cmake_minimum_required(VERSION 3.10)

project(discord)

include_directories(${CMAKE_SOURCE_DIR}/c)
include_directories(${CMAKE_SOURCE_DIR}/cpp)

file(GLOB SOURCES "cpp/*.cpp")

add_library(discord ${SOURCES})

install(TARGETS discord DESTINATION lib)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/c/ DESTINATION include/discord FILES_MATCHING PATTERN "*.h")
install(DIRECTORY ${CMAKE_SOURCE_DIR}/cpp/ DESTINATION include/discord FILES_MATCHING PATTERN "*.h")