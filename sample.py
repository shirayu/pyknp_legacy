#! /bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys
import knp

if __name__ == '__main__':
    sys.stdin  = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    while True:
        tmp = []
        line = u""

        for line in sys.stdin:
            tmp.append(line)
            if line == u"EOS\n":
                break
        if line != u"EOS\n":
            quit()

        sent = knp.Sentence(tmp)
        for bpindex, bp in enumerate(sent.getBasicPhrases()):
            info = bp.getInfo()
            syspas = bp.getPas()
            surf = u"".join(sent.getMorphs(bpindex))

            sys.stdout.write(surf)
            sys.stdout.write(u"\t")
            for k,v in info.items():
                sys.stdout.write(k)
                sys.stdout.write(u":")
                sys.stdout.write(v)
                sys.stdout.write(u" ")
            sys.stdout.write(u"\n")

            if syspas is not None:
                sys.stdout.write(u"s:")
                sys.stdout.write(sent.getSurface())
                sys.stdout.write(u"\t")

                sys.stdout.write(u"p:")
                sys.stdout.write(surf.rstrip(u"．。"))
                sys.stdout.write(u"\t")
                for mycase, val in syspas.items():
                    sys.stdout.write(u"\t")
                    sys.stdout.write(mycase)
                    sys.stdout.write(u":")
                    sys.stdout.write(val[2])
                sys.stdout.write(u"\n")

