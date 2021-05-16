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

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('tk')
    depends_on('tcl')

    phases = ['configure', 'build', 'install']


    def configure(self, spec, prefix):
        # configure = Executable('./Configure')
        configure = Executable('./oommf.tcl pimake distclean')
        configure()
        configure2 = Executable('./oommf.tcl pimake upgrade')
        configure2()


    def build(self, spec, prefix):
        make = Executable('./oommf.tcl pimake ')
        make()

        
    def install(self, spec, prefix):
        # Uses OOMMF's pimake system
        print(spec)
        # Is there a better way then this?
        # cp = Executable('/bin/cp -av . ' + prefix)
        #cp()
        install_tree('.', prefix) 
        
