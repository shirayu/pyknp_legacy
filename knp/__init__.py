#! /bin/env python
# -*- coding:utf-8 -*-

import codecs
import sys

def getKV(tagstr, start=0):
    mydic = {}
    while True:
        ksplitter = tagstr.find(u'="', start)
        if ksplitter == -1:
            break
        key = tagstr[start:ksplitter]
        valend = ksplitter + 2
        while tagstr[valend] != u'"' or tagstr[valend-1]=='\\':
            valend += 1
        val = tagstr[ksplitter+2 : valend]
#        yield key, val
        mydic[key] = val
        start = valend +2

    return mydic

import collections

class PAS(dict):
    def __init__(self, name=None, no=None):
        dict.__init__(self)
        self.name = name
        self.no = no


class BasicPhrase(object):
    def __init__(self, line, position):
        assert isinstance(line, unicode)
        assert line.startswith(u"+ ")

        self.__line = line.rstrip()
        self.__info = {}
        self.__attributes = []
        self.__goldpas = None
#         self.__pas = collections.defaultdict(list)
        self.__pas = None
        self.__position = position

        self.__getInfo()

    def __parsePAS(self, val):
        c0 = val.find(u':')
        c1 = val.find(u':', c0+1)
        cf = val[:c0]
        cfno = val[c0+1:c1]
        self.__pas = PAS(cf, cfno)
    
        if val.count(u":") < 2: #For copula
            return
        
        for k in val[c1+1 : -1].split(u';'):
            items = k.split(u"/")
            if items[1] != u"U" and  items[1] != u"-":
                mycase = items[0]
                mycasetype = items[1]
                myarg = items[2]
                try:
                    myarg_no = int(items[3])
                except:
                    myarg_no = -1 #TODO
                try:
                    myarg_sent_id = int(items[5])
                except:
                    myarg_sent_id = -1 #TODO

                self.__pas[mycase] = {u"no":myarg_no, u"type":mycasetype, u"arg":myarg, u"sid":myarg_sent_id}

    def __getInfo(self):
        second_space_position = self.__line.find(u' ', 2)
        assert second_space_position != -1
        self.__relation = self.__line[2 : second_space_position]

        tag_start = second_space_position +2
        tag_end = second_space_position
        while tag_end != -1:
            tag_end = self.__line.find(u'><', tag_start)
            kv_splitter = self.__line.find(u':', tag_start, tag_end)
            if self.__line[tag_start:].startswith(u'rel '):
                mydic = getKV(self.__line[tag_start:tag_end], 4)
                mytype = mydic[u'type']
                mytarget = mydic[u'target']
                if self.__goldpas is None:
                    self.__goldpas = PAS()
                self.__goldpas[mytype].append(mytarget)
            elif kv_splitter == -1:
                self.__attributes.append(self.__line[tag_start:tag_end])
            else:
                key = self.__line[tag_start : kv_splitter]
                val = self.__line[kv_splitter +1 : tag_end]

                if key == u'格解析結果':
                    self.__parsePAS(val)
                    pass
                else:
                    self.__info[key] = val
            tag_start = tag_end + 2

    def __repr__(self):
        return self.__line

    def getGoldPas(self):
        return self.__goldpas

    def getPas(self):
        return self.__pas

    def getInfo(self):
        return self.__info

    def getPosition(self):
        return self.__position

class Sentence(object):
    def __init__(self, lines):
        self.__morphs = []
        self.__bps = []
        self.__bp2morph = [[0]]
        self._start_position = 0
        self.__bp2start_positions = []
        for line in lines:
            if line.startswith(u";;"):
                pass
            elif line.startswith(u"# "): #new sentence
                pass
            elif line.startswith(u"* "): #new bunsetsu phrase
                pass
            elif line.startswith(u"+ "): #new basic phrase
                self.__bp2morph[-1].append(len(self.__morphs))
                self.__bp2morph.append([len(self.__morphs)])
                self.__bp2start_positions.append(self._start_position)

                mybp = BasicPhrase(line, self._start_position)
                self.__bps.append(mybp)
            elif line == u"EOS\n":
                break
            else:
                first_space_pos = line[:-1].find(u" ")
                self.__morphs.append(line[:first_space_pos])
                self._start_position += len(line[:first_space_pos])

        self.__bp2morph[-1].append(len(self.__morphs))
        self.__bp2morph.append([len(self.__morphs), 0])
        del self.__bp2morph[0]

    def getMorphs(self, bpindex):
        start, end = self.__bp2morph[bpindex]
        return self.__morphs[start:end]

    def getStartPosition(self, bpindex):
        return self.__bp2start_positions[bpindex]

    def getSurface(self):
        return u"".join(self.__morphs)


    def getBasicPhrases(self):
        return self.__bps

class Sentences(list):
    def __init__(self, f):
        tmp = []
        line = u""

        for line in f:
            tmp.append(line)
            if line == u"EOS\n":
                sent = Sentence(tmp)
                self.append(sent)
                tmp = []

import subprocess
import os

class Parser(object):
    def __init__(self, knp_option=""):
        subproc_args = { 'stdin': subprocess.PIPE,
                         'stdout': subprocess.PIPE,
                         'stderr': subprocess.STDOUT,  # not subprocess.PIPE
                         'cwd': '.',
                         'close_fds' : True,          }
        args = 'bash -c "juman | knp -tab %s"' % knp_option
        try:
            env = os.environ.copy()
            self.p = subprocess.Popen(args, env=env, shell=True, **subproc_args)
        except OSError:
            raise 
        (self.stdouterr, self.stdin) = (self.p.stdout, self.p.stdin)

    def __del__(self):
        self.p.stdin.close() #send EOF (This is not obligate)
        try:
            self.p.kill()
            self.p.wait()
        except OSError:
            # can't kill a dead proc
            pass

    def parseSentence(self, sentence):
        self.p.stdin.write(sentence.encode("utf8") + "\n")

        result = []
        while True:
            line = unicode(self.stdouterr.readline()[:-1], "utf8")
            if line == u"EOS":
                break
            result.append(line)
        return result


if __name__ == '__main__':
    pass
