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
        Clock.schedule_interval(self.update, 1)
        self.title = 'fathom'
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source="")
        self.layout.add_widget(self.image)

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

        self.update(dt=None)
        return self.layout

    def update(self, dt):
        # Generate timestamp and signature
        t = str(time.time()).encode("utf-8")
        h = SHA256.new(t)
        signature = pss.new(self.pri_key).sign(h)
        msg = {
            "Signature": base64.b64encode(signature),
            "Timestamp": t,
        }
        print(msg)
        # Generate qrcode of timestamp and signature
        imgIO = io.BytesIO()
        qr = qrcode.make(msg)
        qr.save(imgIO, ext='png')
        imgIO.seek(0)
        imgData = io.BytesIO(imgIO.read())
        # Load qr code into the UI
        self.image.texture = CoreImage(imgData, ext='png').texture
        self.image.reload()


if __name__ == "__main__":
    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    Fathom().run()
