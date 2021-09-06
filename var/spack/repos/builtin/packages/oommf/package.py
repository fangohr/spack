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
    """

    homepage = "https://math.nist.gov/oommf/"
    url = "https://math.nist.gov/oommf/dist/oommf20a2_20200608-hotfix.tar.gz"

    maintainers = ["fangohr"]

    version(
        "20200608-hotfix",
        sha256="5c349de6e698b0c2c5390aa0598ea3052169438cdcc7e298068bc03abb9761c8",
    )

    depends_on("tk", type=("build", "link", "test", "run"))
    depends_on("tcl", type=("build", "link", "test", "run"))
    depends_on("xproto", type=("build"))

    phases = ["configure", "build", "install"]

    # sanity checks: (https://spack.readthedocs.io/en/latest/packaging_guide.html#checking-an-installation)
    sanity_check_is_file = [join_path("bin", "oommf.tcl")]
    sanity_check_is_dir = ["usr/bin/oommf/app", "usr/bin/oommf/app/oxs/eamples"]

    def get_oommf_path(self, prefix):
        """Given the prefix, return the full path of the OOMMF installation below `prefix`."""
        oommfdir = os.path.join(prefix.usr.bin, "oommf")
        return oommfdir

    def configure(self, spec, prefix):
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
        test_env = {}

        # This environment variable (OOMMF_ROOT) seems not to be
        # set at this point, so we have to set it manually for the test:
        oommfdir = self.get_oommf_path(self.prefix)
        test_env["OOMMF_ROOT"] = oommfdir

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
