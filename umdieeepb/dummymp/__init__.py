#!/usr/bin/env python
# DummyMP - Multiprocessing Library for Dummies!
# Copyright 2014 Albert Huang.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# 
# DummyMP Library -
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import time
import sys

from . import config
from .config import DUMMYMP_GENEROUS, DUMMYMP_NORMAL,     \
                                      DUMMYMP_AGGRESSIVE, \
                                      DUMMYMP_EXTREME,    \
                                      DUMMYMP_NUCLEAR
from ._version import *
from .loghandler import *
from .process import *
from .detect import *
from .interface import *
from .taskmgr import *
