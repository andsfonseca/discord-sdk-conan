cmake_minimum_required(VERSION 3.15)

project(discord CXX)

# Path to the downloaded Discord Game SDK
set(DISCORD_SDK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/sdk")

file(GLOB SOURCES "${DISCORD_SDK_DIR}/cpp/*.cpp")

add_library(discord STATIC ${SOURCES})

target_include_directories(discord PUBLIC
    $<BUILD_INTERFACE:${DISCORD_SDK_DIR}/c>
    $<BUILD_INTERFACE:${DISCORD_SDK_DIR}/cpp>
    $<INSTALL_INTERFACE:include/discord>
)

# Link with native Discord Game SDK shared library (per OS/arch)
if(WIN32)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(DISCORD_LIB_DIR "${DISCORD_SDK_DIR}/lib/x86_64")
    else()
        set(DISCORD_LIB_DIR "${DISCORD_SDK_DIR}/lib/x86")
    endif()
    target_link_libraries(discord PUBLIC "${DISCORD_LIB_DIR}/discord_game_sdk.dll.lib")
elseif(APPLE)
    set(DISCORD_LIB_DIR "${DISCORD_SDK_DIR}/lib/x86_64")
    target_link_libraries(discord PUBLIC "${DISCORD_LIB_DIR}/discord_game_sdk.dylib")
elseif(UNIX)
    set(DISCORD_LIB_DIR "${DISCORD_SDK_DIR}/lib/x86_64")
    # Fix: Rename lib
    if(EXISTS "${DISCORD_LIB_DIR}/discord_game_sdk.so" AND
       NOT EXISTS "${DISCORD_LIB_DIR}/libdiscord_game_sdk.so")
        file(RENAME
            "${DISCORD_LIB_DIR}/discord_game_sdk.so"
            "${DISCORD_LIB_DIR}/libdiscord_game_sdk.so")
    endif()
    target_link_libraries(discord PUBLIC "${DISCORD_LIB_DIR}/libdiscord_game_sdk.so")
endif()

# Install targets
install(TARGETS discord DESTINATION lib)
install(DIRECTORY ${DISCORD_SDK_DIR}/c/ DESTINATION include/discord FILES_MATCHING PATTERN "*.h")
install(DIRECTORY ${DISCORD_SDK_DIR}/cpp/ DESTINATION include/discord FILES_MATCHING PATTERN "*.h")