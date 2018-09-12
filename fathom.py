#!/usr/bin/env python
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC, RSA
from Crypto.Signature import DSS, pss
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import base64
import io
import kivy
import numpy
import os.path
import qrcode
import time


class Fathom(App):
    def build(self, pri_key_arg=None, pub_key_arg=None):
        # kivy stuff
        Clock.schedule_interval(self.generateSignature, 1)
        self.title = 'fathom'
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source="")
        self.image.allow_stretch = True
        self.layout.add_widget(self.image)

        # generate keys if necessary
        if not pri_key_arg:
            self.pri_key_arg = "private.pem"
        else:
            self.pri_key_arg = pri_key_arg

        if os.path.isfile(self.pri_key_arg):
            self.pri_key = RSA.import_key(open(self.pri_key_arg))
        else:
            print(("generating private key: {}".format(self.pri_key_arg)))
            self.pri_key_raw = RSA.generate(2048)
            self.pri_key = self.pri_key_raw.export_key()
            file_out = open(self.pri_key_arg, "wb")
            file_out.write(self.pri_key)

        if not pub_key_arg:
            self.pub_key_arg = "public.pem"
        else:
            self.pub_key_arg = pub_key_arg

        if os.path.isfile(self.pub_key_arg):
            self.pub_key = RSA.import_key(open(self.pub_key_arg))
        else:
            print(("generating public key: {}".format(self.pub_key_arg)))
            self.pub_key = self.pri_key_raw.publickey().export_key()
            file_out = open(self.pub_key_arg, "wb")
            file_out.write(self.pub_key)

        # signature objects
        self.time = None
        self.hash = None
        self.signature = None
        self.msg = None

        self.generateSignature(dt=None)
        return self.layout

    def generateChirp(self):
        pass

    def generateQR(self):
        # Generate qrcode of timestamp and signature
        imgIO = io.BytesIO()
        qr = qrcode.QRCode(border=0)
        qr.add_data(self.msg)
        qr.make(fit=True)
        img = qr.make_image(fill_color="white", back_color="black")
        img.save(imgIO, ext='png')
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        # Load qr code into the UI
        self.image.texture = CoreImage(imgData, ext='png').texture
        self.image.reload()

    def generateSignature(self, dt):
        # Generate timestamp and signature
        self.time = str(time.time()).encode("utf-8")
        self.hash = SHA256.new(self.time)
        self.signature = pss.new(self.pri_key).sign(self.hash)
        self.msg = {
            "Signature": base64.b64encode(self.signature),
            "Timestamp": self.time,
        }
        # print(self.msg)
        self.generateChirp()
        self.generateQR()


if __name__ == "__main__":
    # Window.fullscreen = 0
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    Fathom().run()
