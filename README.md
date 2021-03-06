# fathom
## Cryptographic anti-impersonation

Computer hardware and software have recently advanced to the degree that realistic speech synthesis is now available to just about anyone and within a decade the same will apply to graphical synthesis.

Fathom is a tool to which seeks to provide the ability to make digital audio/video impersonation practically impossible if used preemptively.



## Install dependencies
```
$ pip install pycryptodome qrcode
AND
$ sudo apt install python-kivy
OR
$ sudo apt install libgl1-mesa-dev 
$ pip install kivy
```
tested on ubuntu



## Run
```
$ python fathom.py
```



## Use cases
* coming soon



## TODO
- [x] generate public private key pairs and sign utc timestamp.
- [x] encode signed timestamp as qrcode to secure against visual impersonation.
- [ ] choose signature algorithm.
- [ ] encode/play signed timestamp as audio "chirps"(probably ~18khz) to secure against auditory impersonation.
