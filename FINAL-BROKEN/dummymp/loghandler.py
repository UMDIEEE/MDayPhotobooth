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
# DummyMP Library - Logging Redirect Handler
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import logging
import os

from . import config

class DummyMPLogHandler(logging.Handler):
    """DummyMP logging handler to allow multiprocess logging.
    
    This class is a custom logging handler to allow spawned processes 
    (from :py:mod:`multiprocessing`) to log without any issues. This 
    works by intercepting emitted log records, and sending them via 
    queue to the master process. The master process will process each 
    record and call :py:meth:`logging.Logger.handle` to emit the 
    logging record at the master process level.
    
    Note that this class can be used as a general multiprocess logging 
    handler simply by removing the int_pid attribute.
    
    Attributes:
        queue (:py:class:`multiprocessing.Queue`): The Queue object to 
            forward logging records to.
        int_pid (int): The internal PID used to reference the process.
    """
    
    def __init__(self, int_pid, queue):
        """Initializes DummyMPLogHandler with the inputted internal PID
        and Queue object."""
        logging.Handler.__init__(self)
        self.queue = queue
        self.int_pid = int_pid
    
    def emit(self, record):
        """Method override to forward logging records to the internal
        Queue object."""
        try:
            # Format: [ [queueMsgID, PID, internal PID], record ]
            self.queue.put([[config.DUMMYMP_LOG_ID, os.getpid(), self.int_pid], record])
        except:
            # Something went wrong...
            self.handleError(record)
