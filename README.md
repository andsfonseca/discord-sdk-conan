# Discord Game SDK Recipe (discord-sdk-conan)

The Conan 2 recipe (https://conan.io/) for the Discord Game SDK (https://discord.com/developers/docs/game-sdk/sdk-starter-guide), allowing simple integration into C/C++ projects via `find_package()`.

## What is?

Discord Game SDK is a set of native libraries and headers provided by Discord that enable games and native applications to integrate Discord features such as Rich Presence, user authentication, voice, lobbies, and activity management. The SDK ships prebuilt binaries for multiple platforms and exposes a C/C++ API so applications can interact with Discord services at runtime.

> Note: Discord has been migrating functionality from the legacy Game SDK to the newer Discord Social SDK. The Game SDK is considered legacy in many contexts; if you are starting a new integration, check the Discord Social SDK documentation.

## Available Versions

| Version | Windows x86 | Windows x64 | Linux x64 | macOS x64 | macOS ARM64 |
|--------|:-----------:|:-----------:|:---------:|:---------:|:-----------:|
| 3.2.1  | ✅          | ✅          | ✅        | ✅        | ✅          |
| 2.5.6  | ✅          | ✅          | ✅        | ✅        | ❌          |

## Installation 

### From local

Clone this repository and create the package in your local Conan cache:

```bash
git clone https://github.com/<seu-usuario>/conan-discord-game-sdk.git
cd conan-discord-game-sdk

# Latest version (3.2.1)
conan create . --version=3.2.1 --build=missing

# Or older version (2.5.6)
conan create . --version=2.5.6 --build=missing
```

## Usage

### 1. Add dependency to `conanfile.txt`

```ini
[requires]
discord-game-sdk/3.2.1

[generators]
CMakeDeps
CMakeToolchain
```

### 2. Use in CMakeLists.txt

```cmake
find_package(discord CONFIG REQUIRED)

add_executable(meu_app main.cpp)
target_link_libraries(meu_app PRIVATE discord::discord)
```

### 3. Example C++ usage

```cpp
#include <discord/discord.h>

discord::Core* core{};
auto result = discord::Core::Create(CLIENT_ID, DiscordCreateFlags_NoRequireDiscord, &core);
```

### 4. Copy shared library to the output (runtime)

The native shared library needs to be placed next to the executable at runtime.

Example for Windows (copying `discord_game_sdk.dll`):

```cmake
    string(TOUPPER "${CMAKE_BUILD_TYPE}" _DISCORD_BUILD_TYPE_UPPER)
    set(_discord_dll "${discord-game-sdk_PACKAGE_FOLDER_${_DISCORD_BUILD_TYPE_UPPER}}/bin/discord_game_sdk.dll")
    if(EXISTS "${_discord_dll}")
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different "${_discord_dll}" "$<TARGET_FILE_DIR:${PROJECT_NAME}>"
        )
    endif()
```

Example for Linux:

```cmake
string(TOUPPER "${CMAKE_BUILD_TYPE}" _BUILD_TYPE_UPPER)
set(_discord_so "${discord-game-sdk_PACKAGE_FOLDER_${_BUILD_TYPE_UPPER}}/lib/libdiscord_game_sdk.so")
if(EXISTS "${_discord_so}")
    add_custom_command(TARGET meu_app POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different "${_discord_so}" "${CMAKE_CURRENT_BINARY_DIR}"
    )
endif()
```
 
## Issues

Feel free to submit issues and enhancement requests.

## Contribution

1. Fork the project
2. Create a _branch_ for your modification (`git checkout -b my-new-resource`)
3. Do the _commit_ (`git commit -am 'Adding a new resource...'`)
4. _Push_ (`git push origin my-new-resource`)
5. Create a new _Pull Request_ 

## License and Legal Notes

Ownership: The Discord Game SDK binaries and source (when provided by Discord) are the property of Discord, Inc. and are distributed under Discord’s own license and developer terms. By using this Conan recipe you agree to comply with Discord’s [Terms of Service](https://discord.com/developers/docs/policies-and-agreements/developer-terms-of-service). and any license terms that accompany the SDK binaries.

This recipe: The Conan recipe in this repository is provided as a packaging utility and does not change the license of the SDK binaries. The recipe only automates downloading the official SDK artifacts and repackaging them for Conan consumption.

Sources of binaries: The official download URLs and checksums for each SDK version are recorded in conandata.yml. Those URLs point to Discord’s official distribution.

Disclaimer: This repository and recipe are provided “as-is” to simplify integration into C/C++ projects. They are not affiliated with or endorsed by Discord, Inc.

Redistribution: Before redistributing Discord binaries (for example, publishing a Conan package to a public registry), confirm that redistribution is permitted by Discord’s license and developer terms. For this reason, this repository does not include prebuilt binaries or upload packages to public Conan registries.