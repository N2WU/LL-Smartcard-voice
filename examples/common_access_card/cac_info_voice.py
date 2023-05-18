"""
 Copyright 2015, MASSACHUSETTS INSTITUTE OF TECHNOLOGY
 Subject to FAR 52.227-11 – Patent Rights – Ownership by the Contractor (May 2014).
 SPDX-License-Identifier: BSD-3-Clause

    This program dumps general information about a CAC card.
"""
# Navtive
import logging
import optparse
from cryptography.fernet import Fernet
import numpy as np

# LL Smartcard
import llsmartcard.apdu as APDU
from llsmartcard.card import CAC
import voice_process

#do this once, then delete
def create_pin():
    pin = [1,1,1,1,1,1,1,1]
    np.save('pin.npy', pin)

def store_pin():
    # key generation
    key = Fernet.generate_key()
 
    # string the key in a file
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    # opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open('pin.npy', 'rb') as file:
        original = file.read()
        
    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open('pin.npy', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def get_pin():
    # should decrypt a text file or something with the pin
    # using the key
    fernet = Fernet(key)

    # opening the encrypted file
    with open('pin.npy', 'rb') as enc_file:
        encrypted = enc_file.read()
    # decrypting the file
    decrypted = fernet.decrypt(encrypted)
    pin = np.load(decrypted)
    # opening the file in write mode and
    # writing the decrypted data
    with open('pin.npy', 'wb') as dec_file:
        dec_file.write(decrypted)
    return pin

def process_card(connection, options):
    """
        Will dump all of the interesting information from a CAC card to standard
        out
        
        WARNING: The PIN verify command will be sent multiple times.  If the 
        PIN is wrong, it will lock your CAC card!
    """

    # Open card
    card = CAC(connection)

    # Set this to your PIN.  Please be very careful with this!
    verify = voice_process.main()
    if verify == True
        PIN = get_pin() #[0x37, 0x37, 0x37, 0x37, 0x37, 0x37, 0x37, 0x37]
    # Easy enough - change None to a function getPIN(), then getPIN() should roll through everything else
    
    # Print NIST PIV Objects
    print "Printing NIST PIV Objects..."
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.CHUID)
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.CCC)
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.KEY_DIG_SIG)
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.KEY_MNG)
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.KEY_PIV_ATH)
    card.print_object(APDU.APPLET.NIST_PIV,
                      APDU.OBJ_NIST_PIV.SEC_OBJ)

    # Print DOD PIV Object
    print "Printing DoD PIV Objects..."
    card.print_object(APDU.APPLET.DOD_PIV,
                      APDU.OBJ_DOD_PIV.CCC)

    card.print_object(APDU.APPLET.DOD_PIV,
                      APDU.OBJ_DOD_PIV.FNGR_PRNT,
                      pix=APDU.PIX_CAC.PIV_TRNS_APLT)
    card.print_object(APDU.APPLET.DOD_PIV,
                      APDU.OBJ_DOD_PIV.CHUID)

    # Print DOD CAC Objects
    print "Printing DoD CAC Objects..."
    card.print_object(APDU.APPLET.DOD_CAC,
                      APDU.OBJ_DOD_CAC.KEY_PKI_ENC)
    card.print_object(APDU.APPLET.DOD_CAC,
                      APDU.OBJ_DOD_CAC.KEY_PKI_ID)
    card.print_object(APDU.APPLET.DOD_CAC,
                      APDU.OBJ_DOD_CAC.KEY_PKI_SIG)


    # Do we have a PIN to access authenticated information?
    if PIN is not None:
        print "Printing NIST PIV Objects... (PIN PROTECTED)"
        card.print_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.KEY_CRD_ATH,
                          pin=PIN)
        card.print_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.FACE,
                          pin=PIN)
        card.print_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.FNGR_P1,
                          pin=PIN)
        card.print_object(APDU.APPLET.NIST_PIV,
                          APDU.OBJ_NIST_PIV.FNGR_P2,
                          pin=PIN)
        
        print "Printing DoD PIV Objects... (PIN PROTECTED)"
        card.print_object(APDU.APPLET.DOD_PIV,
                          APDU.OBJ_DOD_PIV.SEC_OBJ,
                          pix=APDU.PIX_CAC.PIV_TRNS_APLT,
                          pin=PIN)
        card.print_object(APDU.APPLET.DOD_PIV,
                          APDU.OBJ_DOD_PIV.FACE,
                          pix=APDU.PIX_CAC.PIV_TRNS_APLT,
                          pin=PIN)
        
        print "Printing DoD CAC Objects... (PIN PROTECTED)"
        card.print_object(APDU.APPLET.DOD_CAC,
                          APDU.OBJ_DOD_CAC.CAC_PERSON,
                          pin=PIN)
        card.print_object(APDU.APPLET.DOD_CAC,
                          APDU.OBJ_DOD_CAC.CAC_PERSONEL,
                          pin=PIN)
    


if __name__ == "__main__":

    # Import our command line parser
    from llsmartcard import parser
    opts = optparse.OptionParser()

    # parse user arguments
    parser.command_line(opts, process_card)
