# regentropy
Parses Windows Registry hive files listing the key values with a high entropy.

## Disclaimer
After I'd already written [regsize](https://github.com/bridgeythegeek/regsize), someone mentioned that doing the entropy could be really handy. I can't remember who it was. So, regentropy was their idea, I just brought it to pythonic life. If you are that person, do feel free to remind me and I'll gladly give you the credit.

## Background
The Windows Registry holds thousands upon thousands of entries. Malware has been seen to store executables and public/private keys therein. For example, a CryptoLocker variant stores the public key in the Registry:

- http://watchguardsecuritycenter.com/2013/11/04/everything-you-wanted-to-know-about-cryptolocker/

By listing the Registry key values with a high entropy, an investigator can quickly identify keys that warrant further investigation.
## Requirements
### python-registry
The fantastic python-registry module which does all the heavy lifting of parsing the registry files.
- http://www.williballenthin.com/registry/

#### A Note on Installing from PIP
At the time of writing, pip is serving up python-registry 1.0.4. This is not the latest version. The latest version is [1.1.0a](https://pypi.python.org/pypi/python-registry/1.1.0). However, 1.1.0a is a pre-release and as such, will only be installed if you use the <tt>--pre</tt> switch with the pip command. For example:

```
$ pip install --pre python-registry
```

## Usage
```
usage: regentropy.py [-h] [--min-ent MIN_ENT] [--min-bytes MIN_BYTES] [--csv] target [target ...]

positional arguments:
  target                file to analyse. supports globbing: folder/*

optional arguments:
  -h, --help            show this help message and exit
  --min-ent MIN_ENT, -e MIN_ENT
                        show hits with at least this entropy (default=7.0)
  --min-bytes MIN_BYTES, -b MIN_BYTES
                        ignore data less than this many bytes (default=128)
  --csv, -c             output in CSV format
```
