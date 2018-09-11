from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from PIL import Image, ImageTk
from base64 import b64encode
import os.path
import qrcode
import time
import tkinter as tk


class Fathom(object):
    def __init__(self, pri_key_arg=None, pub_key_arg=None):
        self.pri_key = None
        self.pub_key = None
        self.image_root = tk.Tk()
        self.panel1 = tk.Label(self.image_root, image="")

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

        self.runForever()

    def runForever(self):
        while True:
            t = str(time.time())
            print(t)
            h = SHA256.new(t)
            # this will be used for visual identity verification
            signature = pss.new(self.pri_key).sign(h)
            sig_hex = b64encode(signature)

            sig_img = qrcode.make(sig_hex)
            tkimage = ImageTk.PhotoImage(sig_img)
            self.panel1.configure(image=tkimage)
            self.panel1.image = tkimage
            self.panel1.pack()
            self.image_root.update_idletasks()
            self.image_root.update()
            print(sig_hex)

            # print("---------------------------------------")

            # h = SHA256.new(t)
            # verifier = pss.new(self.pub_key)
            # try:
            #     verifier.verify(h, signature)
            #     print "The signature is authentic."
            # except (ValueError, TypeError):
            #     print "The signature is not authentic."

            time.sleep(2)


if __name__ == "__main__":
    f = Fathom()
    # f.runForever()
