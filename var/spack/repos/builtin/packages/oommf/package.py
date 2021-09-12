
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack import *
from spack.util.executable import Executable


class Oommf(Package):
    """The Object Oriented MicroMagnetic Framework (OOMMF) is aimed at
    developing portable, extensible public domain programs and tools for
    micromagnetics.

    The code forms a completely functional micromagnetics package, with
    the additional capability to be extended by other programmers so that
    people developing new code can build on the OOMMF foundation. OOMMF is
    written in C++, a widely-available, object-oriented language that can
    produce programs with good performance as well as extensibility. For
    portable user interfaces, we make use of Tcl/Tk so that OOMMF operates
    across a wide range of Unix, Windows, and Mac OS X platforms. The main
    contributors to OOMMF are Mike Donahue, and Don Porter.

    Summary taken from OOMMF documentation https://math.nist.gov/oommf/

    OOMMF home page: "https://math.nist.gov/oommf/"

    OOMMF as a git repository: https://github.com/fangohr/oommf

    Versions ending with "-vanilla" indicate that the sources are taken
    directly from https://math.nist.gov/oommf/dist/ . All other versions are
    from the https://github.com/fangohr/oommf (which includes the "-vanilla"
    sources, and adds additional OOMMF extensions). See
    https://github.com/fangohr/oommf for details.
    """

    homepage = "https://math.nist.gov/oommf/"
    # default URL for versions
    url = "https://github.com/fangohr/oommf/archive/refs/tags/20a1_20180930_ext.tar.gz"

    maintainers = ["fangohr"]

    # version from github (uses default url variable)
    version('20a2_20200608', 
            sha256='a3113f2aca0b6249ee99b2f4874f31de601bd7af12498d84f28706b265fa50ab',
            preferred=True)

    version('20a1_20180930_ext',
            sha256='18bf9bd713c7ee6ced6d561ce742d17e0588ae24ef2e56647a5c8a7853e07a4c')

    # (currently most) recent version from OOMMF website
    version( "20a2_20200608-vanilla",
             sha256="5c349de6e698b0c2c5390aa0598ea3052169438cdcc7e298068bc03abb9761c8",
             url =
             "https://math.nist.gov/oommf/dist/oommf20a2_20200608-hotfix.tar.gz" )


    # Deprecated versions have never been tested with spack
    version('20a2_20190930-vanilla',
            sha256='53b41ef30f76766239a1071d13081d8d7604a2ea59187ca4abef356ad1be4986',
            url='https://math.nist.gov/oommf/dist/oommf20a2_20190930.tar.gz',
            deprecated=True)
    
    version('20a1_20180930', deprecated=True,
            sha256='c871e0dbb1522c3c1314af6c084b90cdbe69fd869b55ac94443851b74f818ed2')

    version('20a0_20170929a0', deprecated=True,
            sha256='3439d1c9e95cc7395bc2e2330bba8cf198585d1b350251ea8561c1554ff8c7fd',
            url='https://github.com/fangohr/oommf/archive/refs/tags/2.0a0_20170929a0.tar.gz')

    version('12b0_20160930', deprecated=True,
            sha256='363006f549bb63a39564fafc18b52342a14c1c3769c214467a39f72a0c0be36b',
            url='https://github.com/fangohr/oommf/archive/refs/tags/1.2b0_20160930b1.tar.gz')


    depends_on("tk", type=("build", "link", "test", "run"))
    depends_on("tcl", type=("build", "test", "run"))
    depends_on("xproto", type=("build"))

    phases = ["configure", "build", "install"]

    # sanity checks: (https://spack.readthedocs.io/en/latest/packaging_guide.html#checking-an-installation)
    sanity_check_is_file = [join_path("bin", "oommf.tcl")]
    sanity_check_is_dir = ["usr/bin/oommf/app", "usr/bin/oommf/app/oxs/eamples"]

    def get_oommf_source_root(self):
        """If we download the source from NIST, then 'oommf.tcl' is in the root directory.
        if we download from github, then it is in 'oommf/oommf.tcl'. 

        Here, we try to find the relative path to that file, and return it.
        """
        if 'oommf.tcl' in os.listdir():
            print(f"Found 'oommf.tcl' in {os.getcwd()} "
                  "(looks like source from NIST)")
            return "."
        elif 'oommf.tcl' in os.listdir('oommf'):
            print(f"Found 'oommf.tcl' in {os.getcwd()}/oommf "
                  "(looks like source from Github)")
            return "oommf"
        else:
            raise ValueError(f"Cannot find 'oommf.tcl' in {os.getcwd()}")

    def get_oommf_path(self, prefix):
        """Given the prefix, return the full path of the OOMMF installation
        below `prefix`."""

        oommfdir = os.path.join(prefix.usr.bin, "oommf")
        return oommfdir

    def configure(self, spec, prefix):
        # change into directory with source code
        os.chdir(self.get_oommf_source_root())

        configure = Executable("./oommf.tcl pimake distclean")
        configure()
        configure2 = Executable("./oommf.tcl pimake upgrade")
        configure2()

    def build(self, spec, prefix):
        make = Executable("./oommf.tcl pimake ")
        make()

    def install(self, spec, prefix):
        # keep a copy of all the tcl files and everything oommf created.
        # in OOMMF terminology, this is OOMMF_ROOT
        # We are now using prefix/usr/bin/oommf for that location - is there a better place?
        oommfdir = self.get_oommf_path(prefix)
        install_tree(".", oommfdir)

        # The one file that is used directly by the users should be available as the binary for the user:
        install_files = ["oommf.tcl"]
        mkdirp(prefix.bin)
        for f in install_files:
            install(os.path.join(oommfdir, f), prefix.bin)

    def setup_environment(self, spack_env, run_env):
        """Set OOMMF_ROOT so that oommf.tcl can find its files."""
        oommfdir = self.get_oommf_path(self.prefix)
        run_env.set("OOMMF_ROOT", oommfdir)
        # set OOMMFTCL so ubermag / oommf can find oommf
        run_env.set("OOMMFTCL", join_path(oommfdir, "oommf.tcl"))

    @run_after("install")
    def check_install_version(self):
        spec = self.spec
        test_env = {}

        # Make sure the correct config is found
        # This environment variable (OOMMF_ROOT) seems not to be
        # set at this point, so we have to set it manually for the test:
        oommfdir = self.get_oommf_path(self.prefix)
        test_env["OOMMF_ROOT"] = oommfdir

        print("Testing oommf.tcl +version")

        # where is tcl?
        tclsh = Executable(join_path(spec["tcl"].prefix.bin, "tclsh"))
        # where is oommf.tcl?
        oommf_tcl_path = join_path(spec.prefix.bin, "oommf.tcl")
        # put the command together and execute
        output = tclsh(
            oommf_tcl_path, "+version", output=str.split, error=str.split, env=test_env
        )

        print("output received fromm oommf is '{}".format(output))

    @run_after("install")
    def check_install_platform(self):
        spec = self.spec
        test_env = {}
        # OOMMF needs paths to execute
        test_env["PATH"] = os.environ["PATH"]
        print("PATH=", test_env["PATH"])

        # Make sure the correct config is found
        # This environment variable (OOMMF_ROOT) seems not to be
        # set at this point, so we have to set it manually for the test:
        oommfdir = self.get_oommf_path(self.prefix)
        test_env["OOMMF_ROOT"] = oommfdir

        print("Testing oommf.tcl +platform")

        # where is tcl?
        tclsh = Executable(join_path(spec["tcl"].prefix.bin, "tclsh"))
        # where is oommf.tcl?
        oommf_tcl_path = join_path(spec.prefix.bin, "oommf.tcl")
        # put the command together and execute
        output = tclsh(
            oommf_tcl_path, "+platform", output=str.split, error=str.split, env=test_env
        )

        print("output received fromm oommf is '{}".format(output))

    @run_after("install")
    def check_install_stdprob3(self):
        spec = self.spec
        test_env = {}
        # OOMMF needs paths to execute
        test_env["PATH"] = os.environ["PATH"]
        print("PATH=", test_env["PATH"])

        # Make sure the correct config is found
        # This environment variable (OOMMF_ROOT) seems not to be
        # set at this point, so we have to set it manually for the test:
        oommfdir = self.get_oommf_path(self.prefix)
        test_env["OOMMF_ROOT"] = oommfdir

        print("Testing oommf.tcl standard problem 3")

        # where is tcl?
        tclsh = Executable(join_path(spec["tcl"].prefix.bin, "tclsh"))
        # where is oommf.tcl?
        oommf_tcl_path = join_path(spec.prefix.bin, "oommf.tcl")
        # put the command together and execute
        oommf_examples = join_path(spec.prefix.usr.bin, "oommf/app/oxs/examples")
        task = join_path(oommf_examples, "stdprob3.mif")
        output = tclsh(
            oommf_tcl_path,
            "boxsi",
            "+fg",
            task,
            "-exitondone",
            "1",
            output=str.split,
            error=str.split,
            env=test_env,
        )
        print("output received fromm oommf is '{}".format(output))

    def test(self):
        """Run these smoke tests when requested explicitly"""
        ## run "oommf +version"

        spec = self.spec
        exe = join_path(spec["tcl"].prefix.bin, "tclsh")
        oommf_tcl_path = join_path(spec.prefix.bin, "oommf.tcl")
        options = [oommf_tcl_path, "+version"]
        purpose = "Check oommf.tcl can execute (+version)"
        expected = ["oommf.tcl"]

        self.run_test(
            exe,
            options=options,
            expected=expected,
            status=[0],
            installed=False,
            purpose=purpose,
            skip_missing=False,
            work_dir=None,
        )

        ## run "oommf +platform"

        options = [oommf_tcl_path, "+platform"]
        purpose = "Check oommf.tcl can execute (+platform)"
        expected = [
            "OOMMF threads",
            "OOMMF release",
            "OOMMF API index",
            "Temp file directory",
        ]
        self.run_test(
            exe,
            options=options,
            expected=expected,
            status=[0],
            installed=False,
            purpose=purpose,
            skip_missing=False,
            work_dir=None,
        )

        ## run standard problem 3 with oommf (about 30 seconds runtime)

        purpose = "Testing oommf.tcl standard problem 3"
        print(purpose)

        oommf_examples = join_path(spec.prefix.usr.bin, "oommf/app/oxs/examples")
        task = join_path(oommf_examples, "stdprob3.mif")

        options = [oommf_tcl_path, "boxsi", "+fg", task, "-exitondone", "1"]

        expected = ['End "stdprob3.mif"', "Mesh geometry: 32 x 32 x 32 = 32 768 cells"]
        self.run_test(
            exe,
            options=options,
            expected=expected,
            status=[0],
            installed=False,
            purpose=purpose,
            skip_missing=False,
            work_dir=None,
        )
