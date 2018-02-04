# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 12:05:45 2017

@author: Matthias Höffken
"""

from __future__ import print_function

__all__ = [ "KITTI_PARAM_MODE", "SINTEL_PARAM_MODE", "MIDDLEBURY_PARAM_MODE", \
            "estimateFlow", "cFlowEstimator" ]

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

    imgS = np.ascontiguousarray( img1, dtype=np.float32 )
    imgT = np.ascontiguousarray( img2, dtype=np.float32 )

    mval = max( imgS.max(), imgT.max() )
    if 1 < mval:
        # normalization
        nval = 1. / float(mval)
        
        if imgS is img1:
            imgS = imgS * nval
        else:
            imgS *= nval
        
        if imgT is img2:
            imgT = imgT * nval
        else:
            imgT *= nval
    
    #######
    
    if img1Edges is None:
        imgSEdges = epic.computeSobelEdges( imgS ) * 255.
    else:
        imgSEdges = np.ascontiguousarray( img1Edges, dtype=np.float32 ) * 255.
    
    if imgSEdges is img1Edges:
        allowEdgeModification = False
    else:
        allowEdgeModification = True
    
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
    
    lMatches = cpm.computeCPMFlow( imgS, imgT, n_steps=nCPMSteps )
    flowField = epic.computeEpicFlow( imgS*255, imgT*255, imgSEdges, lMatches, variParams, epicParams, allowEdgeModification )
    
    
    return _denseCPMFlowResStruct( matches=lMatches, flowfield=flowField, variParams=variParams, epicParams=epicParams, nCPMSteps=nCPMSteps )

    
######################################################################################################################


class cFlowEstimator(object):
    
    mCPMSteps = None
    mVariParams = None
    mEpicParams = None
    mEpicParamMode = None
    
    
    def __init__(self, nCPMSteps=3, variParams=None, epicParams=None, epicParamMode=None ):
        self.mCPMSteps = nCPMSteps
        self.mVariParams = variParams
        self.mEpicParams = epicParams
        self.mEpicParamMode = epicParamMode
    
    
    def __apply__(self, img1, img2, img1Edges=None ):
        res = estimateFlow( img1, img2, img1Edges, self.mCPMSteps, self.mVariParams, self.mEpicParams, self.mEpicParamMode )
        self.mVariParams = res.variParams
        self.mEpicParams = res.epicParams
        self.mCPMSteps = res.nCPMSteps
        
        return res
    