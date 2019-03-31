# encoding=utf8
import os
import re


class DAYI4TO3:
    def __init__(self):
        self.buf = []
        self.dayidict = []
        self.filename = ""
        pass

    def write(self, outputname):
        print("bufsize: %d " % len(self.buf))
        with open(outputname, 'w', encoding='utf8') as f:
            for item in self.buf:
                f.write("%s\n" % item)

            f.write("%chardef end")
            f.close()

    def loaddayi(self, name):

        self.filename = name

        startconver = 0
        dayi_re = re.compile(r"(.*)\s(.*)")
        if os.path.exists(name):
            with open(name, encoding='utf8') as f:
                lines = [line.rstrip('\n') for line in f]


                keylist = {}

                inscount = 1

                for l in lines:
                    if startconver is 0:
                        if l.find("%chardef begin"):
                            print("start convert")
                            startconver = 1
                        self.buf.append(l)
                    else:
                        if l[:2] != "##":
                            result = dayi_re.search(l)

                            # add 3 key first
                            if result:
                                dkey = result.group(1).strip()
                                keylist[dkey] = result.group(2).strip()

                        self.buf.append(l)
                
                for n, l in enumerate(lines):
                    if startconver is 0:
                        if l.find("%chardef begin"):
                            print("start convert")
                            startconver = 1
                    else:
                        if l[:2] != "##":
                            result = dayi_re.search(l)

                            # add 3 key first
                            if result:
                                dkey = result.group(1).strip()
                                if len(dkey) is 4:
                                    newdkey = dkey[0:2] + dkey[3]
                                    if newdkey not in keylist:
                                        # print("key %s : %s not in list, insert it" % (newdkey,
                                        #    result.group(2).strip()))
                                        temp = newdkey + "  " + result.group(2).strip()

                                        # rarely situation one key will have two difference 4 key disassemble 
                                        keylist[newdkey] = result.group(2).strip()
                                        self.buf.insert(n + inscount, temp)
                                        inscount += 1



            f.close()

        else:
            print("Cannot find file %s", name)


if __name__ == "__main__":

    dayi = DAYI4TO3()
    dayi.loaddayi("dayi4.cin")
    dayi.write("dayi4-add3.cin")
