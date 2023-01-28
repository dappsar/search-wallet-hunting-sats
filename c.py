# requirements: python, pip, pip install bip32utils mnemonic
# to run: python3 c.py 1
#
# Posibilities: 2**32 = 4.294.967.296 (4K29 Millon keys), (128 bits - (8*12) bits = 32 bits)
# El script arroja: 3043 keys en 60 segs / el total se calcularia en 876 dias.
# La Wallet a obtener es BTC BIP84: bc1q7kw2uepv6hfffhhxx2vplkkpcwsslcw9hsupc6, Path: m/84'/0'/0'/0/0
#
# for TEST:
# wallet: bc1qm4zz7jstwp5x5cqhmljtj76rvy63xglxwslfs2
# seeds: grocery still faith tribe worth bleak furnace raven report prevent young excuse
# generate: 
#   - bip32: Path: m/0'/0'/0 - Address: 16sRpnVnCAy8JKRinVV7UYEXYyqT1peujo
#   - bip44: Path: m/44'/0'/0'/0/0 - Address: 17QtS9Vq95ZpoawFkTdg2Ms3DgG1k1xCzm
#   - bip49: Path: m/49'/0'/0'/0/0 - Address: 3QaYqaqz1HvuXVFXLZtcgPdqhwwMYB1n8S
#   - bip84: Path: m/84'/0'/0'/0/0 - Address: bc1qm4zz7jstwp5x5cqhmljtj76rvy63xglxwslfs2
#   - bip86: Path: m/86'/0'/0'/0/0 - Address: bc1prjdh9lr236n988yf5yx3a2ecnmad096nylr655r073dsnm5qzfmskjgmkh
#
# Se puede ver aquí el detalle de generación para cada path: https://bitcoiner.guide/seed/
#
import os
import sys
import random
import mnemonic.mnemonic as mnemonic
import itertools
import getopt
from datetime import datetime, timedelta
from pycoin.symbols.btc import network as btc
from pycoin.networks.bitcoinish import create_bitcoinish_network as btcnet
from string import hexdigits


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

  #bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
  #bip32_child_key_obj = bip32_root_key_obj
  #.ChildKey(84 + bip32utils.BIP84)
  #.ChildKey(0)
  #.ChildKey(0)
  #.ChildKey(0)
  #.ChildKey(0)

  ACCT84 = '84H/0H/0H'
  HW84 = dict(bip32_pub_prefix_hex="04b24746", bip32_prv_prefix_hex="04b2430c")
  net = btcnet("", "", "", **dict(wif_prefix_hex="80", **HW84))

  acct = net.keys.bip32_seed(seed).subkey_for_path(ACCT84)
  key  = acct.subkey_for_path('0/0')
  hash = key.hash160(is_compressed=True)
  wif  = key.wif()
  xpub = acct.hwif(as_private=False)
  addr = btc.address.for_p2pkh_wit(hash)   
  xprv = acct.hwif(as_private=True)


  return {
    'mnemonic_words': mnemonic_words,
    'addr': addr,
    'publickey': xpub,
    'privatekey': wif
    #'addr': bip32_child_key_obj.Address(),
    #'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
    #'privatekey': bip32_child_key_obj.WalletImportFormat(),
    #'coin': 'BTC'
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


def searchWallet(wallet, words, pswd):
  result = bip39(words.upper(), pswd.upper())
  pk = result['addr']
  sk = result['privatekey']
  match = pk.strip().upper() == wallet.upper()

  if (match):
    return True, pk, sk

  # serach lower case  
  result = bip39(words.lower(), pswd.lower())
  addr = result['addr']
  sk = result['privatekey']
  match = addr.strip().lower() == wallet.lower()

  return match, addr, sk


def process(dicNbr, seeds, pswd, wallet):
  flush = 0
  total = 0
  maxRecords = 1000000
  date1 = datetime.now()

  for i in range(12):
    if (seeds[i] == '*'):
      missingSeed = getUniqueWord(getDict(dicNbr), seeds)
      seeds[i] = missingSeed

  if (pswd == '*'):
    pswd = getUniqueWord(getDict(dicNbr), seeds)

  for c in itertools.permutations(seeds, r=len(seeds)):
    words  = ' '.join(c[:12])
    match, pk, sk = searchWallet(wallet, words, pswd)

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
  # challenge 
  wallet = 'bc1q7kw2uepv6hfffhhxx2vplkkpcwsslcw9hsupc6'
  seeds = ['blast','hollow','state','monkey','elder','argue',
           '*','*','*','*','*','*']
  pswd = 'huntingsats' # Just I guest for now!

  # just for test
  # wallet = 'bc1qm4zz7jstwp5x5cqhmljtj76rvy63xglxwslfs2'
  # seeds = ['grocery','still','faith','tribe','worth','bleak', 
  #          'furnace','raven','report','prevent','young','excuse', ""]
  # pswd = ''

  process(dicNbr, seeds, pswd, wallet)


if __name__ == "__main__":
  main(sys.argv[1:])
