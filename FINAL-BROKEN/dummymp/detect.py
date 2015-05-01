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
# DummyMP Library - CPU availability checker
#   multiprocessing library for dummies!
#   (library for easily running functions in parallel)
# 

import psutil
import logging
import datetime
import os
import time

from . import config

def poll_procs(interval):
    """Poll for processes and return information about them.
    
    Polls all processes and returns a dictionary with information about
    all of the processes.
    
    Args:
        interval (int): Delay before fetching process status. This is
            akin to top -d ##, where a delay is specified.
    
    Returns:
        tuple: Tuple with the first element being a list of Process
        objects, each with a .dict attribute. Each .dict attribute
        contains information about the process, stored in the form of a
        dict. It includes:
        
        * ``'username'``:
            Username of the user who started the process.
        * ``'cpu_percent'``:
            Percent of CPU used by the process.
        * ``'status'``:
            Status of the process (running, stopped, zombie).
        
        The second element in the tuple contains a summary dictionary 
        with the total number of running, stopped, and zombie 
        processes, with keys 'running', 'stopped', and 'zombie', 
        respectively.
        ::
        
            (
                [Process(
                    pid=30159, name='services.exe',
                    dict={'username':USERNAME, ...}
                    ), ...],
                {'running': ##, 'stopped': ##, ...}
            )
        
    """
    # sleep some time
    time.sleep(interval)
    procs = []
    procs_status = {}
    for p in psutil.process_iter():
        try:
            p.dict  = p.as_dict(['username', 'cpu_percent', 'status'])
            try:
                procs_status[p.dict['status']] += 1
            except KeyError:
                procs_status[p.dict['status']] = 1
        except psutil.NoSuchProcess:
            pass
        else:
            procs.append(p)
    
    # return processes sorted by CPU percent usage
    processes = sorted(procs, key=lambda p: p.dict['cpu_percent'],
                       reverse=True)
    return (processes, procs_status)

def needUpdateCPUAvail():
    """Check if the CPU availability needs to be updated.
    
    Utilizing configuration and checking the time elapsed from the
    previous check, determine whether the CPU availability function,
    getCPUAvail(), needs to be run or not to update CPU availability.
    
    Args:
        None
    
    Returns:
        bool: Boolean indicating whether the CPU availability needs to
        be updated or not.
    """
    return not ( \
            (config.DUMMYMP_MODE == config.DUMMYMP_NUCLEAR) or \
            (datetime.datetime.now() - config.LAST_CPU_CHECK <= config.CPU_CHECK_TIMEDELTA_THRESHOLD))

def getSpawnProcPIDs():
    """Fetch all running DummyMP system process IDs.
    
    Looking through all of the DummyMP processes, determine if any are
    running, and if any, retrieve their system process IDs.
    
    Args:
        None
    
    Returns:
        list: An list with the system process IDs of current running
        spawned DummyMP processes.
    """
    pids = []
    for proc in config.dummymp_procs:
        if proc.is_alive():
            pids.append(proc.pid)
    return pids

def getTotalCPUs():
    """Get the total number of CPUs on the system.
    
    Detects and returns the total number of CPUs on the system.
    
    Args:
        None
    
    Returns:
        int: An integer with the number of CPUs that are on the system.
    """
    return psutil.cpu_count()

def getCPUAvail():
    """Get number of CPUs available.
    
    Fetch the number of CPUs available based on the current priority
    and limit configuration.
    
    Args:
        None
    
    Returns:
        int: An integer with the number of CPUs that are available.
    """
    
    # If the time threshold is met, OR we are in NUCLEAR mode, just
    # return the cached CPU availability.
    if (config.DUMMYMP_MODE == config.DUMMYMP_NUCLEAR) or (datetime.datetime.now() - config.LAST_CPU_CHECK <= config.CPU_CHECK_TIMEDELTA_THRESHOLD):
        return config.CPU_AVAIL
    
    # Get number of CPUs!
    ncpus = psutil.cpu_count()
    
    # Initialize array...
    avg = []
    
    # Check to make sure we aren't looking at ourselves!
    if config.total_running == config.CPU_AVAIL:
        return config.CPU_AVAIL
    
    logging.debug("Querying CPUs (%s mode)..." % (config.DUMMYMP_STRING[config.DUMMYMP_MODE]))
    
    # Get PIDs of DummyMP spawned processes!
    dmp_pids = getSpawnProcPIDs()
    
    # Call twice to get accurate measurements...
    cur_state = poll_procs(config.DUMMYMP_MINTERVAL[config.DUMMYMP_MODE])
    cur_state = poll_procs(config.DUMMYMP_MINTERVAL[config.DUMMYMP_MODE])
    
    # Initialize CPU usage array...
    cpu_usage_percents = []
    
    # If the process meets threshold, AND is not a process of DummyMP,
    # add the CPU usage to our list.
    for p in cur_state[0]:
        if (p.dict["cpu_percent"] > config.DUMMYMP_THRESHOLD[config.DUMMYMP_MODE]) and (p.pid != os.getpid()) and (p.pid not in dmp_pids):
            cpu_usage_percents.append(p.dict["cpu_percent"])
    
    # Add up total CPU usage...
    total_cpu_usage = sum(cpu_usage_percents)
    
    # ...and calculate the number of CPUs!
    available_num_cpus = int(((ncpus * 100.0) - total_cpu_usage) / 100.0)
    
    logging.debug("Total external CPU usage: %i%%" % total_cpu_usage)
    logging.debug("Available CPUs: %i/%i" % (available_num_cpus, ncpus))
    
    # Update state
    config.CPU_AVAIL = available_num_cpus
    config.LAST_CPU_CHECK = datetime.datetime.now()
    
    # Return number of CPUs available!
    return available_num_cpus
