# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:05:45 2017

@author: Matthias Höffken
"""

from __future__ import print_function

__all__ = [ "KITTI_PARAM_MODE", "SINTEL_PARAM_MODE", "MIDDLEBURY_PARAM_MODE", \
            "estimateFlow" ]

KITTI_PARAM_MODE="kitti"
SINTEL_PARAM_MODE="sintel"
MIDDLEBURY_PARAM_MODE="middlebury"


import pyCPMFlow as cpm
import pyEpicFlow as epic
import numpy as np


from collections import namedtuple
_denseCPMFlowResStruct = namedtuple("denseCPMFlowRes", "matches flowfield variParams epicParams nCPMSteps")


######################################################################################################################



def estimateFlow( img1, img2, img1Edges=None, nCPMSteps=3, variParams=None, epicParams=None, epicParamMode=None ):
        
    if img1Edges is None:
        img1Edges = epic.computeSobelEdges( img1 )
        allowEdgeModification = True
    else:
        allowEdgeModification = False
    
    img1 = np.ascontiguousarray( img1, dtype=np.float32 )
    img2 = np.ascontiguousarray( img2, dtype=np.float32 )

    
    #######
    
    if (variParams is None) or (epicParams is None):
        if epicParamMode is None:
            setVariParams = epic.defaultVariationalParams()
            setEpicParams = epic.defaultEpicFlowParams()
        elif KITTI_PARAM_MODE == epicParamMode:
            setEpicParams, setVariParams = epic.kittiParams()
        elif SINTEL_PARAM_MODE == epicParamMode:
            setEpicParams, setVariParams = epic.sintelParams()
        elif MIDDLEBURY_PARAM_MODE == epicParamMode:
            setEpicParams, setVariParams = epic.middleburyParams()
        else:
            raise ValueError( "Unknown value (%s) for parameter epicParamMode" % str(epicParamMode) )
        
        if variParams is None:
            variParams = setVariParams
            epicParams = setEpicParams
    
    #######
    
    lMatches = cpm.computeCPMFlow( img1, img2, n_steps=nCPMSteps )
    flowField = epic.computeEpicFlow( img1, img2, img1Edges, lMatches, variParams, epicParams, allowEdgeModification )
    
    
    return _denseCPMFlowResStruct( matches=lMatches, flowfield=flowField, variParams=variParams, epicParams=epicParams, nCPMSteps=nCPMSteps )

    
    
    
    