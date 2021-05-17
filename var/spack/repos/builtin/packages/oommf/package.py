# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install oommf
#
# You can edit this file again by typing:
#
#     spack edit oommf
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os.path

from spack import *


class Oommf(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://math.nist.gov/oommf/dist/oommf20a2_20200608-hotfix.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('20200608-hotfix', sha256='5c349de6e698b0c2c5390aa0598ea3052169438cdcc7e298068bc03abb9761c8')

    depends_on('tk')
    depends_on('tcl')

    phases = ['configure', 'build', 'install']


    def set_oommf_path(self, prefix):
        """Given the prefix, return the full path of the OOMMF installation below `prefix`."""
        oommfdir = os.path.join(prefix.usr.bin, 'oommf')
        return oommfdir
    

    def configure(self, spec, prefix):
        configure = Executable('./oommf.tcl pimake distclean')
        configure()
        configure2 = Executable('./oommf.tcl pimake upgrade')
        configure2()


    def build(self, spec, prefix):
        make = Executable('./oommf.tcl pimake ')
        make()
        

    def install(self, spec, prefix):
        # keep a copy of all the tcl files and everything oommf created.
        # in OOMMF terminology, this is OOMMF_ROOT
        # We are now using prefix/usr/bin/oommf for that location - is there a better place?
        oommfdir = self.set_oommf_path(prefix)
        install_tree('.', oommfdir)

        # The one file that is used directly by the users should be available as the binary for the user:
        install_files = ['oommf.tcl']
        mkdirp(prefix.bin)
        for f in install_files:
            install(os.path.join(oommfdir, f), prefix.bin)


    def setup_environment(self, spack_env, run_env):
        """Set OOMMF_ROOT so that oommf.tcl can find its files."""
        oommfdir = self.set_oommf_path(self.prefix)
        run_env.set('OOMMF_ROOT', oommfdir)

    # XXX TODO Add smoke test (may platform and one quick example)
