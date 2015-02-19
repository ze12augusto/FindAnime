#!/usr/bin/bash

wget http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.1.0.tar.gz
tar -vzxf beautifulsoup4-4.1.0.tar.gz
cd beautifulsoup4-4.1.0
python3.4 setup.py install

wget https://bootstrap.pypa.io/ez_setup.py
python3.4 ez_setup.py

wget https://pypi.python.org/packages/source/j/jellyfish/jellyfish-0.3.4.tar.gz
tar -vzxf jellyfish-0.3.4.tar.gz
cd jellyfish-0.3.4
python3.4 setup.py install