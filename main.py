#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('src')

from general_mining import general_mining
from specific_mining import specific_mining
from data_counter import data_counter
from data_visualization import data_visualization

if __name__ == '__main__':
    general_mining()
    # specific_mining()
    data_counter()
    data_visualization()
