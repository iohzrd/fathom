# fathom
## Cryptographic anti-impersonation

Computer hardware and software have recently advanced to the degree that realistic speech synthesis is now available to just about anyone and within a decade the same will apply to graphical synthesis.

Fathom is a tool to which seeks to provide the ability to make digital audio/video impersonation practically impossible if used preemptively.



## Install dependencies
### general
```
$ pip install pycryptodome qrcode
```
### kivy version
```
$ sudo apt install python-kivy
OR
$ sudo apt install libgl1-mesa-dev 
$ pip install kivy
```



## Run
```
$ python fathom.py
OR
$ python fathom_tk.py
```


## TODO
- [x] generate public private key pairs and sign utc timestamp.
- [x] encode signed timestamp as qrcode to secure against visual impersonation.
- [ ] encode signed timestamp as audio "chirps" to secure against auditory impersonation.
- [ ] choose signature algorithm.