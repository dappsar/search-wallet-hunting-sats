import os
import random
import binascii
import mnemonic.mnemonic as mnemonic
import bip32utils
import itertools

# requirements: python, pip, pip install bip32utils mnemonic
# to run: python3 c.py
def getUniqueWord(dic, currentWords):
  while True:
    word = random.choice(dic)
    if word not in currentWords:
      return word


def getDict():
  dic = []
  with open('./words.txt', 'r') as fwords:
    dic = fwords.read().split('\n')
    random.shuffle(dic)
  return dic


def bip39(mnemonic_words, password = ''):
  mobj = mnemonic.Mnemonic("english")
  seed = mobj.to_seed(mnemonic_words, password)

  bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
  bip32_child_key_obj = bip32_root_key_obj.ChildKey(
    44 + bip32utils.BIP32_HARDEN
  ).ChildKey(
    0 + bip32utils.BIP32_HARDEN
  ).ChildKey(
    0 + bip32utils.BIP32_HARDEN
  ).ChildKey(0).ChildKey(0)

  return {
    'mnemonic_words': mnemonic_words,
    'addr': bip32_child_key_obj.Address(),
    'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
    'privatekey': bip32_child_key_obj.WalletImportFormat(),
    'coin': 'BTC'
  }


def out(pk, sk, words, pswd):
  with open('./EUREKA.txt', 'a') as feureka:
    feureka.write(str(pk+','+sk+','+words+','+pswd))

  publicResult = pk
  print ('****************************************************************')
  print ('****************************************************************')
  print(pk, sk, words, pswd)
  print ('****************************************************************')
  print ('****************************************************************')
  exit(0)


def searchWallet(words, pswd):
  public = '1A9vZ4oPLb29szfRWVFe1VoEe7a2qEMjvJ'
  result = bip39(words.upper(), pswd.upper())
  pk = result['addr']
  sk = result['privatekey']
  match = pk.strip().upper() == public.upper()

  if (match):
    return True, pk, sk

  # serach lower case  
  result = bip39(words.lower(), pswd.lower())
  pk = result['addr']
  sk = result['privatekey']
  match = pk.strip().lower() == public.lower()

  return match, pk, sk


def process():
  flush = 0
  total = 0
  maxRecords = 100000

  seeds = [
    'blast','hollow','*','*','*','*',
    '*','*','*','*','*','*','*']

  for i in range(13):
    if (seeds[i] == '*'):
      missingSeed = getUniqueWord(getDict(), seeds)
      seeds[i] = missingSeed

  for c in itertools.permutations(seeds, r=len(seeds)):
      words  = ' '.join(c[:12])
      pswd  = c[12:][0]
      
      match, pk, sk = searchWallet(words, pswd)

      if (match):
        out(pk, sk, words, pswd)
      else:
        print(total+1, flush+1, words, pswd, pk, sk)
        flush += 1
        if (flush > maxRecords):
          flush = 0
          total += 1


process()
