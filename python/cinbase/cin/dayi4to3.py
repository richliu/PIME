# encoding=utf8
import os
import re
from collections import defaultdict

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

            # dayi4.cin 本身已有 %chardef end，就不要再補一行
            if not self.buf or self.buf[-1].strip() != "%chardef end":
                f.write("%chardef end\n")
            f.close()

    def loaddayi(self, name):

        self.filename = name

        startconver = 0
        dayi_re = re.compile(r"(.*)\s(.*)")
        if os.path.exists(name):
            with open(name, encoding='utf8') as f:
                lines = [line.rstrip('\n') for line in f]

                # keylist = {}
                keylist = defaultdict(list)

                inscount = 1

                for l in lines:
                    if startconver == 0:
                        if "%chardef begin" in l:
                            print("start convert")
                            startconver = 1
                        self.buf.append(l)
                    else:
                        if l[:2] != "##":
                            result = dayi_re.search(l)

                            # add 3 key first
                            if result:
                                dkey = result.group(1).strip()
                                # keylist[dkey] = result.group(2).strip()
                                keylist[dkey].append(result.group(2).strip())

                        self.buf.append(l)

                startconver = 0
                for n, l in enumerate(lines):
                    if startconver == 0:
                        if "%chardef begin" in l:
                            print("start convert")
                            startconver = 1
                    else:
                        if l[:2] != "##":
                            result = dayi_re.search(l)

                            # add 3 key first
                            if result:
                                dkey = result.group(1).strip()
                                dword = result.group(2).strip()

                                if len(dkey) == 4:
                                    newdkey = dkey[0:2] + dkey[3]
                                    toinsert = 0
                                    if newdkey not in keylist:
                                        toinsert = 1
                                    else:
                                        if dword not in keylist[newdkey]:
                                            toinsert = 1

                                    if toinsert == 1:
                                        print("key %s(%s) : %s not in list, insert it" % (newdkey, dkey,
                                            result.group(2).strip()))
                                        temp = newdkey + "  " + result.group(2).strip()

                                        # rarely situation one key will have two difference 4 key disassemble
                                        # keylist[newdkey] = result.group(2).strip()
                                        keylist[newdkey].append(result.group(2).strip())
                                        self.buf.insert(n + inscount, temp)
                                        inscount += 1

            f.close()

        else:
            print("Cannot find file %s", name)


if __name__ == "__main__":

    dayi = DAYI4TO3()
    dayi.loaddayi("dayi4.cin")
    dayi.write("dayi4-add3.cin")
