![python](https://img.shields.io/badge/python-informational?style=flat&logo=python&logoColor=white&color=6aa6f8)
![bitcoin](https://img.shields.io/badge/bitcoin-informational?style=flat&logo=bitcoin&logoColor=white&color=6aa6f8)


# search-wallet-hunting-sats

## Introduction

hunting Sats Challenge to find wallet based on its seed words!

- A bitcoin wallet with a 12-word BIP-39 seed and a passphrase was created with millions of sats.
- Each word from the wallet backup, mnemonic seed and passphrase, were distributed to 12 partners.
- Each partner will randomly reveal their word on Twitter with [#HuntingSats](https://twitter.com/search?q=HuntingSats&src=typed_query), in late January 2023.
- As words are revealed, anyone can brute force the backup to find the wallet & earn millions of sats.
- Every time a word is publicly revealed, brute forcing gets easier & time to crack the wallet shrinks!
- All words revealed by partners will be shared on [this website](https://www.huntingsats.com/#updates) along with timestamps of public release.


- Wallet: [bc1q7kw2uepv6hfffhhxx2vplkkpcwsslcw9hsupc6](http://mempoolhqx4isw62xs7abwphsq7ldayuidyx2v2oethdhhj6mlo2r6ad.onion/address/bc1q7kw2uepv6hfffhhxx2vplkkpcwsslcw9hsupc6)
- Satoshis in wallet (before cracked): 0.04048285 BTC

More infor [here](https://www.huntingsats.com/#updates)


The Python script in this report helps to find correct secret key and crack the wallet!

---

## Technology Stack & Tools

- Visual Studio Code
- python3 / pip
- Libraries: [bip32utils](https://pypi.org/project/bip32utils/), [mnemonic](https://pypi.org/project/mnemonic/), itertools, random & binascii.


## Setting Up
### 1. Install [python](https://www.python.org/downloads/)

### 2. Install [pip](https://pip.pypa.io/en/stable/installation/)

### 2. Install Dependencies
`$ pip install bip32utils mnemonic`


### Start 

In a terminal execute: 

`$ python c.py`

---

# References Links

- [How I checked over 1 trillion mnemonics in 30 hours to win a bitcoin](https://medium.com/@johncantrell97/how-i-checked-over-1-trillion-mnemonics-in-30-hours-to-win-a-bitcoin-635fe051a752)

