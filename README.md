# PyKNP: KNP module for Python


## Introduction

This is a Python interface to the Japanese Dependency and Case Structure Analyzer [KNP](http://nlp.ist.i.kyoto-u.ac.jp/?KNP).
Differently from other implementations, it does not need to launch a KNP server manually in advance, because this executes KNP internally.
This also accepts raw KNP-parsed texts.

## Requirements

This currently works only for Python 2.

## Installation and Usage

You can install this module in the general way.

    sudo python setup.py install

## Sample

```
python ./sample.py < ./sample.knp
```


## Acknowledgement

I developed this program as a part of the research project 
["Establishment of Knowledge-Intensive Structural Natural Language Processing and Construction of Knowledge Infrastructure"](http://nlp.ist.i.kyoto-u.ac.jp/CREST/?en)
in [Kyoto University](http://www.kyoto-u.ac.jp/en)
supported by [CREST, JST](http://www.jst.go.jp/kisoken/crest/en/).


## Developer
- Yuta Hayashibe

## License
- (c) Yuta Hayashibe 2014
- GNU GENERAL PUBLIC LICENSE Version 3
