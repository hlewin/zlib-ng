from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

import os

equired_conan_version = ">=1.33.0"

class ZlibNgConan(ConanFile):
    name = "zlib-ng"
    version = "2.1.6"
    
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

    no_copy_source = True
    python_requires = "wdyConanHelper/[]"
    python_requires_extend = "wdyConanHelper.ConanCMake"

    def validate(self):
        if self.options.zlib_compat and not self.options.with_gzfileop:
            raise ConanInvalidConfiguration("The option 'with_gzfileop' must be True when 'zlib_compat' is True.")

    def cmake_definitions(self):
        return {
            "ZLIB_ENABLE_TESTS": False,
            "ZLIB_COMPAT": self.options.zlib_compat,
            "WITH_GZFILEOP": self.options.with_gzfileop,
            "WITH_OPTIM": self.options.with_optim,
            "WITH_NEW_STRATEGIES": self.options.with_new_strategies,
            "WITH_NATIVE_INSTRUCTIONS": self.options.with_native_instructions,
            "WITH_SANITIZER": "False",
            "WITH_GTEST": "False",
            "ZLIBNG_ENABLE_TESTS": "False",
        }
