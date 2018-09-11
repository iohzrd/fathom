# fathom
## Cryptographic anti-impersonation

Computer hardware and software have recently advanced to the degree that realistic speech synthesis is now available to just about anyone and within a decade the same will apply to graphical synthesis.

Fathom is a tool to which seeks to provide the ability to make digital audio/video impersonation practically impossible if used preemptively.



## Install dependencies
```
$ pip install pycryptodome qrcode
```



## Run
```
$ python fathom.py
```


## TODO
- [x] generate public private key pairs and sign utc timestamp.
- [x] encode signed timestamp as qrcode to secure against visual impersonation.
- [ ] encode signed timestamp as audio "chirps" to secure against auditory impersonation.