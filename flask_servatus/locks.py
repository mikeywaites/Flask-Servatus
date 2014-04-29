"""
Copyright (c) Django Software Foundation and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of Django nor the names of its contributors may be used
to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
Portable file locking utilities.

Based partially on example by Jonathan Feignberg <jdf@pobox.com> in the Python
Cookbook, licensed under the Python Software License.

    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65203

Example Usage::

    >>> from flask_servatus import locks
    >>> with open('./file', 'wb') as f:
    ...     locks.lock(f, locks.LOCK_EX)
    ...     f.write('Foo')
"""

__all__ = ('LOCK_EX', 'LOCK_SH', 'LOCK_NB', 'lock', 'unlock')

system_type = None

try:
    import win32con
    import win32file
    import pywintypes
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()
    system_type = 'nt'
except (ImportError, AttributeError):
    pass

try:
    import fcntl
    LOCK_EX = fcntl.LOCK_EX
    LOCK_SH = fcntl.LOCK_SH
    LOCK_NB = fcntl.LOCK_NB
    system_type = 'posix'
except (ImportError, AttributeError):
    pass


def fd(f):
    """Get a filedescriptor from something which could be a file or an fd."""
    return f.fileno() if hasattr(f, 'fileno') else f

if system_type == 'nt':
    def lock(file, flags):
        hfile = win32file._get_osfhandle(fd(file))
        win32file.LockFileEx(hfile, flags, 0, -0x10000, __overlapped)

    def unlock(file):
        hfile = win32file._get_osfhandle(fd(file))
        win32file.UnlockFileEx(hfile, 0, -0x10000, __overlapped)
elif system_type == 'posix':
    def lock(file, flags):
        fcntl.lockf(fd(file), flags)

    def unlock(file):
        fcntl.lockf(fd(file), fcntl.LOCK_UN)
else:
    # File locking is not supported.
    LOCK_EX = LOCK_SH = LOCK_NB = None

    # Dummy functions that don't do anything.
    def lock(file, flags):
        pass

    def unlock(file):
        pass
