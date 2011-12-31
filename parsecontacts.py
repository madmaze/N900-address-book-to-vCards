#!/usr/bin/env python3
import re, sys

def toUTF8(input):
#    return bytes.fromhex(input.group(0).replace('\\','')).decode('utf-8')
    return input.group(0).replace('\\','=').upper()

def prefixUTF8(input):
    print(input.group(0))
    sys.exit(0)
    #'\1;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:\2'

def readDBFile(filename):
    f = open(filename)
    infile = f.read()
    f.close()
    # substitute newlines
    infile = infile.replace(r'\0d\0a', '\n')
    return infile

def createVcards(contacts):
    for i,vcard in enumerate(contacts):
    	#print vcard
        vcard = vcard.strip()
        out = ''
        for line in vcard.splitlines(True):
            out = out+ re.sub(r'\A(N|ADR|URL|NOTE|LABEL|FN):([\u0020-\u0080]*[^\u0000-\u0080]+[\u0020-\u0080]*)',
                              r'\1;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:\2',
                              line,
                              re.UNICODE)
        vcard = re.sub(r'\\[0-9a-f]{2}\\[0-9a-f]{2}', toUTF8, out)
        try:
            f = open('vcf/%i.vcf' % i, 'w', encoding='ascii')
        except:
            print("Something failed, exiting. (Hint: does vcf/ exist?")
            sys.exit(-1)
        f.write(vcard+ '\r\n')
        f.close()

def main():
    if (len(sys.argv) == 2):
    	    
    	    contacts = readDBFile(sys.argv[1])
    	    contacts = contacts.split('END:VCARD')
    	    f = open('out.vcf', 'w')
    	    for vc in contacts:
    	    	    try:
    	    	    	    if vc.find("@reply.facebook.com")==-1:
    	    	    	    	    print "BEGIN:VCARD"+vc.split('BEGIN:VCARD')[1]+"END:VCARD"
    	    	    	    	    f.write("BEGIN:VCARD"+vc.split('BEGIN:VCARD')[1]+"END:VCARD\n")
    	    	    except:
    	    	    	    print ""
	    ## split at \00
	    ##contacts = contacts.split(r'\00')
	    ## every other contains only an ID
	    #contacts = contacts[1:-1:2]
	    f.close()
	    print len(contacts)
	
	    ##createVcards(contacts)
    else:
    	    print "Usage: "+sys.argv[0]+" addressbook.db"

if __name__ == "__main__":
    main()
    

