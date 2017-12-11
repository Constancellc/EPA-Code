import urllib
f = open('00000001.jpg','wb')
f.write(urllib.urlopen('https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/13423818_110025622759285_4051836409962595564_n.jpg?oh=8b34c677a8dd573c4e1c41f0b5890c7d&oe=5923AE93').read())
f.close()

