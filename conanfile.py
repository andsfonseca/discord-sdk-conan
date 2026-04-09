from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get, copy, rename
import os


class DiscordGameSDKConan(ConanFile):
    """
    Conan package for the Discord Game SDK
    """
    name = "discord-game-sdk"
    description = "Discord Game SDK"
    license = "Proprietary (Discord Game SDK License)"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"
    exports_sources = "CMakeLists.txt"

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            strip_root=False, destination="sdk")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _get_lib_arch_folder(self):
        """
        Determine the correct library folder based on the OS and architecture.

        Returns:
            str: The name of the library folder.
        """
        if self.settings.os == "Windows":
            if self.settings.arch == "x86_64":
                return "x86_64"
            else:
                return "x86"
        else:
            return "x86_64"

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # Copy library by OS/arch
        lib_arch = self._get_lib_arch_folder()
        src_lib_dir = os.path.join(self.source_folder, "sdk", "lib", lib_arch)

        if self.settings.os == "Windows":
            copy(self, "*.dll.lib", src=src_lib_dir,
                 dst=os.path.join(self.package_folder, "lib"))
            copy(self, "*.dll", src=src_lib_dir,
                 dst=os.path.join(self.package_folder, "bin"))
        elif self.settings.os == "Linux":
            # Fix: Renaming discord_game_sdk.so -> libdiscord_game_sdk.so
            so_src = os.path.join(src_lib_dir, "discord_game_sdk.so")
            so_dst = os.path.join(src_lib_dir, "libdiscord_game_sdk.so")
            if os.path.exists(so_src) and not os.path.exists(so_dst):
                rename(self, so_src, so_dst)
            copy(self, "libdiscord_game_sdk.so", src=src_lib_dir,
                 dst=os.path.join(self.package_folder, "lib"))
        elif self.settings.os == "Macos":
            copy(self, "*.dylib", src=src_lib_dir,
                 dst=os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]

        self.cpp_info.libs = ["discord", "discord_game_sdk"]

        self.cpp_info.set_property("cmake_file_name", "discord")
        self.cpp_info.set_property("cmake_target_name", "discord::discord")

        if self.settings.os == "Windows":
            self.cpp_info.bindirs = ["bin"]

        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]