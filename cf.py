# requirements: python, pip, pip install bip32utils mnemonic pycoin
# to run: python3 c.py -d2
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
# Se puede ver el detalle de generacion para cada path en: https://bitcoiner.guide/seed/
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


def bip39(mnemonic_words, passphrase = ''):
  mobj = mnemonic.Mnemonic("english")
  seed = mobj.to_seed(mnemonic_words, passphrase)

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


def searchWallet(wallet, words, pswd, sUpper=False, sLower=False):
  result = bip39(words, pswd)
  pk = result['addr']
  sk = result['privatekey']
  match = pk.strip().upper() == wallet.upper()

  if (match):
    return True, pk, sk

  if (sUpper):
    # search upper case
    result = bip39(words.upper(), pswd.upper())
    pk = result['addr']
    sk = result['privatekey']
    match = pk.strip().upper() == wallet.upper()

    if (match):
      return True, pk, sk

  if (sLower):
    # search lower case  
    result = bip39(words.lower(), pswd.lower())
    pk = result['addr']
    sk = result['privatekey']
    match = addr.strip().lower() == wallet.lower()

  return match, pk, sk


def process(dicNbr, seeds, wallet, sUpper, sLower):
  flush = 0
  total = 0
  maxRecords = 1000000
  date1 = datetime.now()
  
  for i in range(len(seeds)):
    if (seeds[i] == '*'):
      seeds[i] = getUniqueWord(getDict(dicNbr), seeds)

  for c in itertools.permutations(seeds, r=len(seeds)):
    words  = ' '.join(c[:12])
    pswd  = c[12:][0]
    match, pk, sk = searchWallet(wallet, words, pswd, sUpper, sLower)

    now = str(datetime.now() - date1)
    print(now, total+1, flush+1, words, pswd, pk, sk)
    flush += 1
    if (flush > maxRecords):
      flush = 0
      total += 1

    if (match): 
      out(pk, sk, words, pswd)


def getInputParams(argv):
  dicNbr = 1
  wordsListNbr = 1
  sUpper = False
  sLower = False
  command = 'python c3.py -d <dictionary number (1, 2, or 3)> -w <words list number to use (1, 2, or 3)> -u <search upperCase (True or False)> -l <search lowerCase (True or False)>'
  example = 'python c3.py -d1 -w1 -uFalse -lFalse'

  try:
    opts, args = getopt.getopt(argv,"hd:w:u:l:",["ddictionary=", "wwordListNbr=", "usearchUpper=", "usearchLower=" ])
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
    elif opt in ("-w", "--wwordListNbr"):
      wordsListNbr = arg
    elif opt in ("-u", "--usearchUpper"):
      sUpper = arg
    elif opt in ("-l", "--lserchLower"):
      sLower = arg
  
  if (len(sys.argv) <= 2):
      print ("Error: Tiene que pasar un argumento con el numero de diccionario.y el numero de lista para las palabras")
      print (command)
      print (example)
      sys.exit()
  
  if (int(dicNbr) < 1 or int(dicNbr) > 3):
    dicNbr = 1

  if (int(wordsListNbr) < 1 or int(wordsListNbr) > 6):
    wordsListNbr = 1

  if (sUpper != False or sUpper != True):
    sUpper = False

  if (sLower != False or sLower != True):
    sLower = False

  return int(dicNbr), int(wordsListNbr), sUpper, sLower


def main(argv):
  dicNbr, wordsListNbr, sUpper, sLower = getInputParams(argv)
  # challenge 
  wallet = 'bc1q7kw2uepv6hfffhhxx2vplkkpcwsslcw9hsupc6'
  seeds = []

  if (wordsListNbr == 1):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','wood','hold','just','*']

  if (wordsListNbr == 2):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','wood','hold','timber','*']

  if (wordsListNbr == 3):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','wood','hold','lake','*']

  if (wordsListNbr == 4):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','fire','hold','just','*']

  if (wordsListNbr == 5):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','fire','hold','timber','*']

  if (wordsListNbr == 6):
    seeds = ['blast','hollow','state','monkey', 'select', 'elder','present',
            'argue','horse','fire','hold','lake','*']

  # passphrase is one of the word in array
  process(dicNbr, random.sample(seeds,13), wallet, sUpper, sLower)

if __name__ == "__main__":
  main(sys.argv[1:])

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

# 1. blast, cryptoSteel
# 2. hollow, cointkite
# 3. state, BTCPay
# 4. monkey, BullBitcoin, 25-01 03:34 pm
# 5. select, wasabi wallet, 26-01 12:26 pm
# 6. elder, BlockStream 26-01 01:11 pm
# 7. present, holdHodl, 26-01 04:00 pm
# 8. argue, bitcoinReserve, 27-01 01:55 pm
# 9. horse, memPool, 27-01, 02:09 pm
#! 10. wood, wizardSardine, 28-01, 02:15 pm (no esta confirmado si es wood, podría ser fire tambien)
#! 11. profit o hold, trezor, 29-01 11:29 am (la tiraron en forma de acertijo)
#! 12. just o timber o lake, bitcoin takeover, 29-01, 14.23 (tiraorn 3 una sola es correcta)
#! 13.

#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

