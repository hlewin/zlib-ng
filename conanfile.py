from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

import os

equired_conan_version = ">=1.33.0"

class ZlibNgConan(ConanFile):
    name = "zlib-ng"
    version = "2.0.6"
    
    description = "zlib data compression library for the next generation systems"
    url = "https://gitlab.worldiety.net/worldiety/customer/wdy/libriety/cpp/forks"
    homepage = "https://github.com/zlib-ng/zlib-ng/"
    license ="Zlib"
    topics = ("zlib", "compression")
    
    exports_sources = ["*"]
    generators = "cmake",
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "zlib_compat": [True, False],
               "with_gzfileop": [True, False],
               "with_optim": [True, False],
               "with_new_strategies": [True, False],
               "with_native_instructions": [True, False],
               "fPIC": [True, False]}
    default_options = {"shared": True,
                       "zlib_compat": True,
                       "with_gzfileop": True,
                       "with_optim": True,
                       "with_new_strategies": True,
                       "with_native_instructions": False,
                       "fPIC": True}
    _cmake = None


    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd


    def validate(self):
        if self.options.zlib_compat and not self.options.with_gzfileop:
            raise ConanInvalidConfiguration("The option 'with_gzfileop' must be True when 'zlib_compat' is True.")

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
        self._cmake.definitions["ZLIB_ENABLE_TESTS"] = False
        self._cmake.definitions["ZLIB_COMPAT"] = self.options.zlib_compat
        self._cmake.definitions["WITH_GZFILEOP"] = self.options.with_gzfileop
        self._cmake.definitions["WITH_OPTIM"] = self.options.with_optim
        self._cmake.definitions["WITH_NEW_STRATEGIES"] = self.options.with_new_strategies
        self._cmake.definitions["WITH_NATIVE_INSTRUCTIONS"] = self.options.with_native_instructions

        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        #FIXME: CMake targets are https://github.com/zlib-ng/zlib-ng/blob/29fd4672a2279a0368be936d7cd44d013d009fae/CMakeLists.txt#L914
        suffix = "" if self.options.zlib_compat else "-ng"
#        self.cpp_info.names["pkg_config"] = "zlib" + suffix
        if self.settings.os == "Windows":
            static_flag = "static" if not self.options.shared and tools.Version(self.version) >= "2.0.5" else ""
            build_type = "d" if self.settings.build_type == "Debug" else ""
            self.cpp_info.libs = ["zlib{}{}{}".format(static_flag, suffix, build_type)]
        else:
            self.cpp_info.libs = ["z{}".format(suffix)]
        if self.options.zlib_compat:
            self.cpp_info.defines.append("ZLIB_COMPAT")
        if self.options.with_gzfileop:
            self.cpp_info.defines.append("WITH_GZFILEOP")
        if not self.options.with_new_strategies:
            self.cpp_info.defines.extend(["NO_QUICK_STRATEGY", "NO_MEDIUM_STRATEGY"])
        pkg_config_dir = os.path.join(self.package_folder, "lib/pkgconfig")
        self.output.info(f"Adding {pkg_config_dir} to PKG_CONFIG_PATH")

