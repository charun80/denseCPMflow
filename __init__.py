# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:04:43 2017

@author: Matthias Höffken
"""



__all__ = ["KITTI_PARAM_MODE", "SINTEL_PARAM_MODE", "MIDDLEBURY_PARAM_MODE", \
            "estimateFlow", \
            "writeMatches", "readMatches", \
            "computeSobelEdges", \
            "IllegalEpicFlowArgumentError", \
            "defaultVariationalParams", "defaultEpicFlowParams", \
            "sintelParams", "kittiParams", "middleburyParams" ]

            
            
import os
import sys
sys.path.append( os.path.join( os.path.dirname( os.path.abspath(__file__) ), '_epicflow' ) )
sys.path.append( os.path.join( os.path.dirname( os.path.abspath(__file__) ), '_cpm' ) )

from pyCPMFlow import writeMatches, readMatches
from pyEpicFlow import computeSobelEdges, \
                       IllegalEpicFlowArgumentError, \
                       defaultVariationalParams, defaultEpicFlowParams, sintelParams, kittiParams, middleburyParams
from combinedEstimation import *
