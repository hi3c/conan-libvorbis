from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class LibvobisConan(ConanFile):
    name = "libvorbis"
    version = "1.3.5"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = "libogg/1.3.2@hi3c/experimental"

    def source(self):
        tools.download("http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.gz", "libvorbis.tar.gz")
        tools.unzip("libvorbis.tar.gz")
        os.remove("libvorbis.tar.gz")

    def build(self):
        atbe = AutoToolsBuildEnvironment(self)
        atbe.configure(configure_dir="libvorbis-1.3.5", args=["--with-pic"])
        atbe.make()

    def package(self):
        self.copy("*.h", dst="include", src="libvorbis-1.3.5/include")
        self.copy("*.lib", dst="lib", keep_path=False)

        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["vorbisfile", "vorbis"]
