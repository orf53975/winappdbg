#!~/.wine/drive_c/Python25/python.exe

# Acknowledgements:
#  Nicolas Economou, for his ptool suite on which this tool is inspired.

# Process memory map
# Copyright (c) 2009, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# $Id$

import os
import sys

from winappdbg import Process, System, CrashDump, HexInput

def main():
    print "Process memory map"
    print "by Mario Vilas (mvilas at gmail.com)"
    print

    if len(sys.argv) != 2:
        script = os.path.basename(sys.argv[0])
        print "  %s <pid>" % script
        print "  %s <process.exe>" % script
        return

    System.request_debug_privileges()

    try:
        pid = HexInput.integer(sys.argv[1])
    except:
        s = System()
        s.scan_processes()
        pl = s.find_processes_by_filename(sys.argv[1])
        if not pl:
            print "Process not found: %s" % sys.argv[1]
            return
        if len(pl) > 1:
            print "Multiple processes found for %s" % sys.argv[1]
            for p,n in pl:
                print "\t%12d: %s" % (p,n)
            return
        pid = pl[0][0].get_pid()

    p = Process(pid)
    memoryMap = p.get_memory_map()
    print CrashDump.dump_memory_map(memoryMap),

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    main()
