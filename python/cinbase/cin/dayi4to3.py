# encoding=utf8
import os
import re


class DAYI4TO3:
    def __init__(self):
        self.buf = []
        self.dayidict = []
        self.filename = ""
        pass

    def write(self):
        print("bufsize: %d " % len(self.buf))
        with open(self.filename + ".tmp", 'w', encoding='utf8') as f:
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
                                dkey = result.group(1)
                                if len(dkey) is 4:
                                    temp = dkey[0:2] + dkey[3] + " " + result.group(2)
                                    self.buf.append(temp)

                        self.buf.append(l)
            f.close()

        else:
            print("Cannot find file %s", name)


if __name__ == "__main__":

    dayi = DAYI4TO3()
    dayi.loaddayi("thdayi.cin")
    dayi.write()
