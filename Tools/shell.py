import struct

from adb import adb_commands
from adb import adb_protocol
from adb import usb_exceptions

from usb.core import find as finddev
import os
import sys
import time

from PIL import Image
import numpy as np

class Shell():
    def __init__(self):
        self.dev = finddev(idVendor=0x18d1, idProduct=0x4ee2)
        self.dev.reset()
        self.BANNER = "mobile"

        # KitKat+ devices require authentication
        #signer = sign_m2crypto.M2CryptoSigner(
        #    op.expanduser('~/.android/adbkey'))
        # Connect to the device
        self.device = adb_commands.AdbCommands()
        self.device.ConnectDevice(banner=self.BANNER)

    @classmethod
    def _MakeSyncHeader(self, command, *int_parts):
        command = self._ConvertCommand(command)
        return struct.pack(b'<%dI' % (len(int_parts) + 1), command, *int_parts)

    @classmethod
    def _MakeWriteSyncPacket(self, command, data=b'', size=None):
        if not isinstance(data, bytes):
            data = data.encode('utf8')
        return self._MakeSyncHeader(command, size or len(data)) + data

    @classmethod
    def _ExpectSyncCommand(self, write_commands, read_commands):
        usb = common_stub.StubUsb()
        self._ExpectConnection(usb)
        self._ExpectOpen(usb, b'sync:\0')

        while write_commands or read_commands:
            if write_commands:
                command = write_commands.pop(0)
                self._ExpectWrite(usb, b'WRTE', LOCAL_ID, REMOTE_ID, command)

            if read_commands:
                command = read_commands.pop(0)
                self._ExpectRead(usb, b'WRTE', REMOTE_ID, LOCAL_ID, command)

        self._ExpectClose(usb)
        return usb

    def shellReset(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        time.sleep(5)

    def Close(self):
        return self.device.Close()

    def pullShell(self, remote, local):
        dir_name_screen = os.path.join(os.getcwd(), "screenshot")
        path = os.path.join(dir_name_screen, "{}".format(local))
        try:
            shell = self.device.Shell("screencap -p /sdcard/temp_screen.png")
        except:
            pass

        time.sleep(2)
        try:
            progress = self.device.Pull("/sdcard/temp_screen.png", path, progress_callback="progress %s")
        except:
            for i in range(0, 5):
                try:
                    progress = self.device.Pull("/sdcard/temp_screen.png", path, progress_callback="progress %s")
                    if progress:
                        break
                    else:
                        pass
                except:
                    time.sleep(1)
                    pass
            progress = False

        if progress:
            for i in range(0, 3):
                try:
                    imgpil = Image.open(path)
                    img = np.asarray(imgpil)
                    return imgpil
                except:
                    correctif = self.pullShell(remote, local)
                    return correctif

        #self.device.Pull(remote, local, timeout)

    def inputShell(self, cmd, timeout, repeat=False):
        global dev
        global device

        if repeat:
            for i in range(0, repeat):
                try:
                    cmd = self.device.Shell(cmd, timeout)
                    time.sleep(0.05)
                    return cmd
                except (usb_exceptions.ReadFailedError,
                        adb_protocol.InvalidResponseError,
                        AttributeError):
                    time.sleep(0.02)
                except usb_exceptions.WriteFailedError:
                    self.device = self.shellReset()
                    time.sleep(1)
                    try:
                        cmd = self.device.Shell(cmd, timeout)
                        time.sleep(0.05)
                        return cmd
                    except:
                        time.sleep(0.02)
        else:
            try:
                cmd = self.device.Shell(cmd, timeout)
                time.sleep(0.35)
                return cmd
            except (usb_exceptions.ReadFailedError,
                    adb_protocol.InvalidResponseError,
                    AttributeError):
                time.sleep(0.15)
            except usb_exceptions.WriteFailedError:
                self.device = self.shellReset()
                time.sleep(1)
                try:
                    cmd = self.device.Shell(cmd, timeout)
                    time.sleep(0.30)
                    return cmd
                except:
                    time.sleep(0.10)


    def compute_average_image_color(self, img):
        width, height = img.size

        r_total = 0
        g_total = 0
        b_total = 0

        count = 0
        for x in range(0, width):
            for y in range(0, height):
                r, g, b, o = img.getpixel((x,y))
                r_total += r
                g_total += g
                b_total += b
                count += 1

        return (r_total/count, g_total/count, b_total/count)
