from conans import ConanFile, tools, CMake
from conan.tools.files import get

class DiscordGameSDKConan(ConanFile):
    name = "discord-game-sdk"
    description = "Discord Game SDK"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt"

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):

        cmake = CMake(self)
        cmake.install()

        if self.settings.os == "Windows":
            if self.settings.arch == "x86_64":
                self.copy("*.dll.lib", dst="lib", src="lib/x86_64")
                self.copy("*.dll", dst="lib", src="lib/x86_64")
            else:
                self.copy("*.dll.lib", dst="lib", src="lib/x86")
                self.copy("*.dll", dst="lib", src="lib/x86")
        elif self.settings.os == "Linux":
            self.copy("*.so", dst="lib", src="lib/x86_64")
        elif self.settings.os == "Macos":
            self.copy("*.dylib", dst="lib", src="lib/x86_64")

    def package_info(self):
        
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]

        self.cpp_info.libs = tools.collect_libs(self)

        self.cpp_info.set_property("cmake_target_name", "discord")
        self.cpp_info.set_property("cmake_file_name", "discord")
        self.cpp_info.set_property("cmake_target_namespace", "discord")

        # Old generators
        self.cpp_info.names["cmake_find_package"] = "discord"
        self.cpp_info.names["cmake_find_package_multi"] = "discord"
        
