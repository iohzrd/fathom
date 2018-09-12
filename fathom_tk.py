from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
import PIL
from PIL import Image, ImageTk
from Tkinter import *
import base64
import os.path
import qrcode
import time
import tkinter as tk


class Fathom(object):
    def __init__(self, pri_key_arg=None, pub_key_arg=None):
        self.window = tk.Tk()
        self.window.geometry("%dx%d+0+0" %
                             (self.window.winfo_screenwidth(),
                              self.window.winfo_screenheight()))
        self.canvas = Canvas(
            self.window, bd=0, highlightthickness=0, background='black')

        if not pri_key_arg:
            self.pri_key_arg = "private.pem"
        else:
            self.pri_key_arg = pri_key_arg

        if os.path.isfile(self.pri_key_arg):
            self.pri_key = RSA.import_key(open(self.pri_key_arg).read())
        else:
            print("generating private key: {}".format(self.pri_key_arg))
            self.pri_key_raw = RSA.generate(2048)
            self.pri_key = self.pri_key_raw.export_key()
            file_out = open(self.pri_key_arg, "wb")
            file_out.write(self.pri_key)

        if not pub_key_arg:
            self.pub_key_arg = "public.pem"
        else:
            self.pub_key_arg = pub_key_arg

        if os.path.isfile(self.pub_key_arg):
            self.pub_key = RSA.import_key(open(self.pub_key_arg).read())
        else:
            print("generating public key: {}".format(self.pub_key_arg))
            self.pub_key = self.pri_key_raw.publickey().export_key()
            file_out = open(self.pub_key_arg, "wb")
            file_out.write(self.pub_key)

        while True:
            t = str(time.time()).encode("utf-8")
            h = SHA256.new(t)
            signature = pss.new(self.pri_key).sign(h)
            msg = {
                "Signature": base64.b64encode(signature),
                "Timestamp": t,
            }
            self.qr = qrcode.make(msg)

            if self.window.winfo_width() > self.window.winfo_height():
                smaller = self.window.winfo_height()
            else:
                smaller = self.window.winfo_width()

            self.image = PIL.ImageTk.PhotoImage(
                self.qr._img.resize((smaller, smaller)))
            self.canvas.create_image(
                (self.window.winfo_width() / 2 - smaller / 2),
                (self.window.winfo_height() / 2 - smaller / 2),
                image=self.image,
                anchor=NW)
            self.canvas.pack(fill=BOTH, expand=1)
            self.window.update()
            print(msg)

            time.sleep(1)


if __name__ == "__main__":
    Fathom()
