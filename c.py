# requirements: python, pip, pip install bip32utils mnemonic
# to run: python3 c.py
#
# Posibilities: 2**32 = 4.294.967.296 (4K29 Millon keys), (128 bits - (8*12) bits = 32 bits)
# El script arroja: 3043 keys en 60 segs / el total se calcularia en 876 dias.

import os
import sys
import random
import binascii
import mnemonic.mnemonic as mnemonic
import bip32utils
import itertools
import getopt
from datetime import datetime, timedelta

def getUniqueWord(dic, currentWords):
  while True:
    word = random.choice(dic)
    if word not in currentWords:
      return word


def getDict(dicNbr):
  dic = []
  dicName = './words.'+str(dicNbr)+'.txt'

  with open(dicName, 'r') as fwords:
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


def process(dicNbr):
  flush = 0
  total = 0
  maxRecords = 1000000
  date1 = datetime.now()

  seeds = [
    'blast','hollow','state','monkey','elder','argue',
    '*','*','*','*','*','*','*']

  for i in range(13):
    if (seeds[i] == '*'):
      missingSeed = getUniqueWord(getDict(dicNbr), seeds)
      seeds[i] = missingSeed

  for c in itertools.permutations(seeds, r=len(seeds)):
      words  = ' '.join(c[:12])
      pswd  = c[12:][0]
      
      match, pk, sk = searchWallet(words, pswd)

      if (match):
        out(pk, sk, words, pswd)
      else:
        now = str(datetime.now() - date1)
        print(now, total+1, flush+1, words, pswd, pk, sk)
        flush += 1
        if (flush > maxRecords):
          flush = 0
          total += 1


def getInputParams(argv):
  dicNbr = 1
  command = 'python c.py -d <dictionary number (1, 2, or 3)>'
  example = 'python c.py -d1'

  try:
    opts, args = getopt.getopt(argv,"hd:",["ddictionary="])
  except getopt.GetoptError:
    print ('Number of arguments: ' + str(len(sys.argv)) +  ' arguments.')
    print ('Argument List: ' + str(sys.argv))
    print (command)
    print (example)
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print (command)
      print (example)
      sys.exit()
    elif opt in ("-d", "--ddictionary"):
      dicNbr = arg

  if (len(sys.argv) == 1):
      print ("Error: Tiene que pasar un argumento con el numero de diccionario.")
      print (command)
      print (example)
      sys.exit()
  
  if (int(dicNbr) < 1 or int(dicNbr) > 3):
    dicNbr = 1

  return dicNbr


def main(argv):
  dicNbr = getInputParams(argv)
  process(dicNbr)


if __name__ == "__main__":
  main(sys.argv[1:])
