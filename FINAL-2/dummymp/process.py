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
# DummyMP Library - Process Wrapper
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import os
import time
import logging

from . import config
from .loghandler import *

def _runner(process_id, dummymp_queue, func, *args, **kwargs):
    """Multiprocess function wrapper for running a function given args.
    
    This function wraps an existing function with its args, and allows 
    for additional fields related to multiprocessing. In particular, 
    the internal process ID and the :py:class:`multiprocessing.Queue`
    object are added to facilitate communication between the subprocess
    and the master process.
    
    Args:
        process_id (int): The internal process ID for the particular
            process. This is NOT the actual system process ID.
        dummymp_queue (:py:class:`multiprocessing.Queue`): The Queue
            object that the process should send data to. The Queue
            should be a Queue made specifically for this process.
        func (function): The function that the process should call.
        *args: The arguments that should be passed to the function.
    
    Returns:
        Nothing... but the function will periodically send messages to
        the Queue in this format:
            [ [ DUMMYMP_MSG_TYPE_ID, SYSTEM_PID, INTERNAL_ID ], DATA... ]
        
        Possible DUMMYMP_MSG_TYPE_IDs include:
            DUMMYMP_LOG_ID: ID for log records. The entire format is:
                
                [ [ DUMMYMP_LOG_ID, SYSTEM_PID, INTERNAL_ID ], LOGGING_RECORD ]
                
                When a message of this type is sent, the corresponding
                LOGGING_RECORD is emitted at the master process level.
                (In plain English: the logging message gets sent to the
                main process, and is printed from there.)
            
            DUMMYMP_RET_ID: ID for return data. The entire format is:
                
                [ [ DUMMYMP_RET_ID, SYSTEM_PID, INTERNAL_ID ], RETURN_VAL ]
                
                When a message of this type is sent, the RETURN_VAL is 
                stored in a dictionary at the master process level to 
                archive the return value from this process for future 
                retrieval. (In plain English: the return values are 
                sent to the main process, and are stored in a 
                dictionary for reference.)
        
    """
    # Get the default logger
    logger = logging.getLogger()
    
    # Set to DEBUG so that we get ALL messages
    logger.setLevel(logging.DEBUG)
    
    # Switch out the logging handler...
    
    # First, remove existing handlers...
    hdlrs = logger.handlers
    for hdlr in hdlrs:
        logger.removeHandler(hdlr)
    
    # Initialize our DummyMPLogHandler...
    dmp_handler = DummyMPLogHandler(process_id, dummymp_queue)
    
    # ...and then add that handler instance to the main logger!
    logger.addHandler(dmp_handler)
    
    # Call the function!
    ret = func(*args, **kwargs)
    
    # Send the return value through the queue!
    dummymp_queue.put([ [config.DUMMYMP_RET_ID, os.getpid(), process_id], ret ])
    
    # Pause to avoid losing queue (may be a race condition bug?)
    time.sleep(0.1)
