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
# DummyMP Library - Interface for programs
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 
# TODO: Potentially add interface for killing individual processes?
#       This would require some changes in config.py and taskmgr.py
#       for enhanced information, paricularly with internal process ID
#       tracking.
# 

from multiprocessing import Process, Queue
import copy
import sys

from . import config
from . import _version
from .taskmgr import process_queue

if sys.version_info[0] >= 3:
    # This must be imported for reload() to work
    from imp import reload

def set_max_processes(max_proc):
    """Set maximum processors for DummyMP to use.
    
    Set the maximum number of processors/CPUs for DummyMP to use. 
    Regardless of priority mode, the number of processors/CPUs it takes 
    advantage of will be capped at the number you specify.
    
    Args:
        max_proc (int): Integer specifying the maximum number of 
            processors (or CPUs) for DummyMP to use.
    """
    config.max_processes = max_proc

def get_max_processes():
    """Get maximum processors for DummyMP to use.
    
    Fetch and return the maximum number of processors/CPUs for DummyMP 
    to use.
    
    Args:
        None
    
    Returns:
        int: Integer specifying the current maximum number of 
        processors (or CPUs) for DummyMP to use.
    """
    return config.max_processes

def set_priority_mode(mode):
    """Set the priority mode for DummyMP.
    
    Set the priority mode for DummyMP. The priority mode controls how 
    conscious DummyMP is of other running processes on the system.
    
    Available modes:
    
        DUMMYMP_GENEROUS   - Generous mode.
                             Very conservative about using any CPU, and 
                             ensures that no one else is disrupted. 
                             Note that this is VERY GENEROUS - if all 
                             CPUs are taken, DummyMP will wait until 
                             there are available CPUs! (All other modes 
                             will run a single process, regardless of 
                             CPU usage.) This is the slowest mode!
        DUMMYMP_NORMAL     - Normal mode.
                             Careful not to take up too much resources 
                             on the CPU, but it will try to get things 
                             done. This is faster than GENEROUS, but it 
                             isn't the fastest. This mode is the 
                             default and is recommended for most 
                             conditions.
        DUMMYMP_AGGRESSIVE - Aggressive mode.
                             This mode considers other users, but it 
                             may spawn processes anyway depending on 
                             how other processes behave. This is faster 
                             than NORMAL, and is recommended for 
                             semi-important conditions.
        DUMMYMP_EXTREME    - Extreme mode.
                             This mode somewhat considers other users, 
                             but unless the other processes are using a 
                             significant portion of the CPU, it will 
                             spawn processes anyway. This is faster 
                             than AGGRESSIVE, and is recommended for 
                             important conditions.
        DUMMYMP_NUCLEAR    - Nuclear mode.
                             This mode does NOT consider other users, 
                             and just runs as many processes as it can 
                             allow (total number of cores). This is 
                             much faster than EXTREME, and is 
                             recommended for really important 
                             conditions. Note that this may earn you 
                             very angry co-workers knocking down your 
                             door with pitchforks, so use sparingly!
    
    Regardless of priority mode, if the number of CPUs to use is 
    specified, the number of processors/CPUs it takes advantage of will 
    always be capped at the maximum number specified.
    
    Args:
        mode (int): Integer constant specifying the mode for DummyMP to 
            use.
    """
    config.DUMMYMP_MODE = mode

def set_start_callback(callback):
    """Set the process starting callback for DummyMP.
    
    Set the callback for DummyMP to call when a process is initially
    started.
    
    The callback is called with the following arguments:  
    (config.total_completed, config.total_running, config.total_procs)
    
    * ``total_completed``: Total processes completed.
    * ``total_running``: Total processes currently running.
    * ``total_procs``: Total processes overall, regardless of whether
      they are running or not.
    
    Args:
        callback (function): Function callback to call when a process 
            starts.
    """
    config.PROCESS_START_CALLBACK = callback

def set_end_callback(callback):
    """Set the process completion callback for DummyMP.
    
    Set the callback for DummyMP to call when a process has completed.
    
    The callback is called with the following arguments:
    (config.total_completed, config.total_running, config.total_procs)
    
    * ``total_completed``: Total processes completed.
    * ``total_running``: Total processes currently running.
    * ``total_procs``: Total processes overall, regardless of whether
      they are running or not.
    
    Args:
        callback (function): Function callback to call when a process
            has completed.
    """
    config.PROCESS_END_CALLBACK = callback

def get_priority_mode():
    """Get the priority mode that DummyMP is using.
    
    Fetch and return the priority mode integer constant that DummyMP is
    using.
    
    Args:
        None
    
    Returns:
        int: Integer constant specifying the priority mode integer 
        constant that DummyMP is using.
    """
    return config.DUMMYMP_MODE

def get_version():
    """Get DummyMP's version
    
    Fetch and return the DummyMP library version.
    
    Args:
        None
    
    Returns:
        str: String specifying the DummyMP library version.
    """
    return _version.__version__

def get_returns():
    """Get function returns from completed function runs.
    
    Fetch and return a dictionary of function returns from completed
    function runs. The dictionary is indexed by call order, zero
    indexed.
    
    Args:
        None
    
    Returns:
        dict: Dictionary of function returns, indexed by call order, 
        and zero indexed.
    """
    return config.dummymp_rets

def killall():
    """Kill all currently running processes and remove them from queue.
    
    Kill all of the currently running processes and remove them from 
    the internal running queue.
    
    Args:
        None
    """
    # Clear out all of the processes!
    while len(config.dummymp_procs) != 0:
        # Pick the first one
        dummymp_proc = config.dummymp_procs[0]
        
        try:
            # Attempt to terminate...
            dummymp_proc.terminate()
        except:
            pass
        
        # Run process_queue() once to get any queue items
        process_queue()
        
        # Remove the queue and process
        pi = config.dummymp_procs.index(dummymp_proc)
        config.dummymp_queues.pop(pi)
        config.dummymp_procs.pop(pi)
        
        # Add to the completed count and remove from running count...
        config.total_completed += 1
        config.total_running -= 1
        
        # Make any callbacks, if necessary.
        if config.PROCESS_END_CALLBACK:
            config.PROCESS_END_CALLBACK(config.total_completed, config.total_running, config.total_procs)
            

def reset():
    """Reset DummyMP state and kill all currently running processes.
    
    This resets the DummyMP state, clearing any configuration or state 
    data set. Before resetting, this will kill all of the currently 
    running processes and remove them from the internal running queue. 
    (This calls :py:func:`killall()` before resetting.)
    
    Args:
        None
    """
    killall()
    reload(config)

def set_args_deepcopy(tf):
    """Set whether to deepcopy arguments or not.
    
    Change whether DummyMP will deepcopy the arguments or not. If it is 
    disabled, it is up to the user to ensure that a copy of the 
    arguments is preserved for further use.
    
    Args:
        tf (bool): Boolean indicating whether to enable argument
            deepcopy or not.
    """
    config.DUMMYMP_ARGS_DEEPCOPY = tf

def set_kwargs_deepcopy(tf):
    """Set whether to deepcopy keyword arguments or not.
    
    Change whether DummyMP will deepcopy the keyword arguments or not. 
    If it is disabled, it is up to the user to ensure that a copy of 
    the keyword arguments is preserved for further use.
    
    Args:
        tf (bool): Boolean indicating whether to enable keyword 
            argument deepcopy or not.
    """
    config.DUMMYMP_KWARGS_DEEPCOPY = tf

def run(func, *args, **kwargs):
    """Run a function with multiprocessing.
    
    Run a function with multiprocessing. This actually queues the 
    function and its arguments for running - you need to run 
    :py:func:`.process_process()` or :py:func:`.process_until_done()` 
    in order to actually execute the function.
    
    Args:
        func (function): Function to run.
        args (*args): Arguments to use with the function.
        kwargs (**kwargs): Keyword arguments to use with the function.
    """
    # We need to perform a deepcopy, since we want the original
    # arguments before running! Without a deepcopy, list, dict, and
    # possibly other arguments could be changed, making the function
    # call invalid!
    if config.DUMMYMP_ARGS_DEEPCOPY:
        final_args_tuple = copy.deepcopy(args)
    else:
        final_args_tuple = args
    
    if config.DUMMYMP_KWARGS_DEEPCOPY:
        final_kwargs = copy.deepcopy(kwargs)
    else:
        final_kwargs = kwargs
    
    # Convert args tuple to a list
    final_args   = []
    for final_arg in final_args_tuple:
        final_args.append(final_arg)
    
    # Create our start entry
    start_entry = [ config.total_procs, func, final_args, final_kwargs ]
    
    # Append our start entry!
    config.dummymp_start_procs.append(start_entry)
    
    # Increment total process count
    config.total_procs += 1
