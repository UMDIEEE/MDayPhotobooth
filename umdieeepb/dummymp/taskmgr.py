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
# DummyMP Library - Task Manager
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import logging
import time
from multiprocessing import Process, Queue

from . import config
from .detect import *
from .process import _runner

def process_queue():
    """Process inter-process messages.
    
    Process the inter-process :py:class:`multiprocessing.Queue` 
    objects, which receive messages from the spawned process for 
    logging events and function returns.
    
    Args:
        None
    
    Note:
        Warnings are emitted to log if an invalid message is received.
    """
    # Get main process logger
    logger = logging.getLogger()
    
    # Loop through queues...
    for dummymp_queue in config.dummymp_queues:
        # Make sure there's something to fetch from the queue!
        if not dummymp_queue.empty():
            # Make a request to get the queue, with a timeout to ensure
            # no blocking (or long waiting)
            qout = dummymp_queue.get(timeout = 0.001)
            
            # Check if it's a list or not
            if type(qout) != list:
                logger.warning("WARNING: Received invalid message from process! This may be a bug! Message: %s" % str(qout))
                continue
            
            # Check the message type IDs!
            # Format: [ [ DUMMYMP_MSG_TYPE_ID, SYSTEM_PID, INTERNAL_ID ], DATA... ]
            if qout[0][0] == config.DUMMYMP_LOG_ID:
                # Append PID info text
                qout[1].msg = ("[PID %i] " % qout[0][1]) + qout[1].msg
                # Emit the modified log record
                # BUG: seems like logger.handle() doesn't do any
                # filtering - therefore, we need to filter it ourselves.
                if logger.isEnabledFor(qout[1].levelno):
                    logger.handle(qout[1])
            elif qout[0][0] == config.DUMMYMP_RET_ID:
                # Store return into return dictionary
                config.dummymp_rets[qout[0][2]] = qout[1]
            else:
                logger.warning("WARNING: Received invalid message from process! (Invalid message type ID!) This may be a bug! Message: %s" % str(qout))

def process_process():
    """Process the execution queue and inter-process messages.
    
    Process the execution queue by starting processes in said queue, 
    handle processes that have completed, and process inter-process 
    messages via :py:func:`process_queue()`.
    
    (In plain English: start the queued processes, check processes to 
    see if they are done running, and grab any inter-process messages 
    sent from the spawned process.)
    
    Args:
        None
    
    Returns:
        bool: A boolean indicating whether the execution queue has 
        completed or not. Returns True if it has completed, False if it 
        has not. This return value can be used in a while loop to block 
        until processes have completed. (This is somewhat similar to 
        multiprocessing's :py:meth:`multiprocessing.Process.join()` if
        used in a loop.)
    """
    nproc = 0
    
    # Get main process logger
    logger = logging.getLogger()
    
    # Loop through processes via index!
    while nproc < len(config.dummymp_procs):
        dummymp_proc = config.dummymp_procs[nproc]
        
        # Check if process is complete! (In this case, ensure that
        # the process is not in a start queue and it isn't alive
        # anymore!)
        if (not dummymp_proc in config.dummymp_start_procs) and (not dummymp_proc.is_alive()):
            # Run process_queue() to fetch the remaining queue items
            # from the process.
            process_queue()
            
            # Remove the queue and process
            pi = config.dummymp_procs.index(dummymp_proc)
            
            # Make sure to close the queue!
            
            # ...but first, check to make sure the queue is empty.
            if not config.dummymp_queues[pi].empty():
                process_queue()
            
            # Once we're sure, let's close things up!
            config.dummymp_queues[pi].close()
            config.dummymp_queues.pop(pi)
            config.dummymp_procs.pop(pi)
            
            logger.debug("Process complete!")
            
            # Add to the completed count and remove from running count...
            config.total_completed += 1
            config.total_running -= 1
            
            # Make any callbacks, if necessary.
            if config.PROCESS_END_CALLBACK:
                config.PROCESS_END_CALLBACK(config.total_completed, config.total_running, config.total_procs)
            
            # Deincrement index counter, since we just removed a process
            # from the list.
            nproc -= 1
        
        # Increment
        nproc += 1
    
    # Fetch available CPUs
    avail_cpus = getCPUAvail() - config.total_running
    
    # Check if we need to update CPU avail
    if not needUpdateCPUAvail():
        nproc = 0
        # Loop through process execution queue
        while nproc < len(config.dummymp_start_procs):
            dummymp_proc_entry = config.dummymp_start_procs[nproc]
            
            # Check to make sure we can meet max_processes limit
            # (0 means no limit set)
            if (config.max_processes == 0) or (config.total_running < config.max_processes):
                
                # If there's no available CPUs, check to make sure that a
                # process isn't already running, and that the mode set is
                # not GENEROUS.
                if ((avail_cpus == 0) and (config.total_running == 0) and (config.DUMMYMP_MODE != config.DUMMYMP_GENEROUS)):
                    # Force a single process to run!
                    avail_cpus += 1
                    logger.debug("Not in generous mode, so forcing one task to run.")
                
                # Check if we have any available (or "available") CPUs!
                if avail_cpus > 0:
                    logger.debug("%i CPUs available, spawning process!" % avail_cpus)
                    
                    # Deincrement counter
                    avail_cpus -= 1
                    
                    # Setup Queue
                    # We create the Queue and Process here so that we can
                    # prevent the error from opening too many Queue objects
                    # in multiprocessing.Pipe:
                    #   IOError: handle out of range in select()
                    # Bug: http://bugs.python.org/issue10527
                    q = Queue()
                    
                    # Extract internal PID, function, final_args, and
                    # final_kwargs
                    int_pid = dummymp_proc_entry[0]
                    func = dummymp_proc_entry[1]
                    final_args = dummymp_proc_entry[2]
                    final_kwargs = dummymp_proc_entry[3]
                    
                    # Now add some arguments to the front:
                    # Function to actually run
                    final_args.insert(0, func)
                    # Queue
                    final_args.insert(0, q)
                    # Process ID
                    final_args.insert(0, int_pid)
                    
                    # Create Process object
                    p = Process(target = _runner, args = final_args, kwargs = final_kwargs)
                    
                    # Save it
                    config.dummymp_queues.append(q)
                    config.dummymp_procs.append(p)
                    
                    # Start the process...
                    p.start()
                    
                    # ...and remove it from the starting queue.
                    config.dummymp_start_procs.remove(dummymp_proc_entry)
                    
                    # Increment running counter...
                    config.total_running += 1
                    
                    # Make any callbacks, if necessary.
                    if config.PROCESS_START_CALLBACK:
                        config.PROCESS_START_CALLBACK(config.total_completed, config.total_running, config.total_procs)
                    
                    # Deincrement index counter, since we just removed a process
                    # from the start queue list.
                    nproc -= 1
            else:
                logger.debug("Max processes limit of %i reached, waiting for process to terminate." % config.max_processes)
            
            # Increment
            nproc += 1
    
    # Check to see if we are done!
    if len(config.dummymp_procs) == 0:
        logger.debug("All processes complete, returning True.")
        return True
    return False

def process_until_done():
    """Process the execution queue until all have been completed.
    
    Process the execution queue until it has indicated that all 
    processes in the queue have been completed. (This is somewhat 
    similar to multiprocessing's 
    :py:meth:`multiprocessing.Process.join()`.)
    
    Args:
        None
    """
    # Run process_queue() and process_process() until process_process()
    # returns False (when it completes the process queue)
    while not process_process():
        process_queue()
        time.sleep(0.001)
