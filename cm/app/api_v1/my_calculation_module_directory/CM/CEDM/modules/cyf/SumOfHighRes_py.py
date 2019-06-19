'''
Created on Apr 20, 2017

@author: simulant
'''

import numpy as np
import time 
#cimport numpy as np

DTYPE1 = np.int
#ctypedef np.int_t DTYPE1_t

DTYPE2 = np.float32
#ctypedef np.float64_t DTYPE2_t

#cimport cython

import os
 

def convert_vector(vector,type):
    try:
        if vector.dtype == type:
            pass
            return vector
        if vector.ndim == 1:
            vector1 = np.zeros(vector.shape[0],dtype=type)
            vector1[:] = vector
        else:
            vector1 = np.zeros(vector.shape,dtype=type)
            vector1[:,:] = vector
    except:
        vector1 = type(vector)
    return(vector1)

def CalcAverageBased(HighResM,
                     ResolutionFactor,
                     NumberOfLoops,
                     WeightFaktor, 
                     AdditionalWeightMatrix):
    
    HighResM = convert_vector(HighResM, DTYPE2)
    ResolutionFactor = convert_vector(ResolutionFactor, DTYPE1)
    NumberOfLoops = convert_vector(NumberOfLoops, DTYPE1)
    WeightFaktor = convert_vector(WeightFaktor, DTYPE2)
    AdditionalWeightMatrix = convert_vector(WeightFaktor, DTYPE2)
    r = HighResM.shape[0]
    c = HighResM.shape[1]
    
    rLow = r / ResolutionFactor
    cLow = c / ResolutionFactor
    
    (LowResSumOrig) = CoreLoopSumLowRes(HighResM, 
                        ResolutionFactor)
    #print ("-----")
    #print ("-----")
    #print (np.sum(HighResM))
    print (np.sum(LowResSumOrig))
    #print ("-----")
    #print ("-----")
    
    correction_factor = 1 + 4 * WeightFaktor * (1 + 1/ 1.41)
    WeightFaktor /= correction_factor
    WeightFaktor2 = WeightFaktor / 1.41
    
    HighResM_new = np.zeros((r, c), dtype= DTYPE2)
    LowResSumNew = np.zeros((r/ResolutionFactor, c/ResolutionFactor), dtype= DTYPE2)
    
    print ("CoreLoopCalcAverageBased: Run %i Loops" % NumberOfLoops)
    for i in range(NumberOfLoops):
        for r_ in range(r):
            for c_ in range(c):
                HighResM[r_, c_] *= AdditionalWeightMatrix[r_, c_]
        
        st = time.time()
        for r_ in range(r):
            HighResM_new[r_, 0] = HighResM[r_, 0]
            HighResM_new[r_, c-1] = HighResM[r_, c-1]
        for c_ in range(c):
            HighResM_new[0, c_] = HighResM[0, c_]
            HighResM_new[r-1, c_] = HighResM[r-1, c_]
        for r_ in range(1, r-1):
            for c_ in range(1, c-1):
                
                TEMP_Val = HighResM[r_+1,c_]
                TEMP_Val += HighResM[r_-1,c_]
                TEMP_Val += HighResM[r_,c_+1]
                TEMP_Val += HighResM[r_,c_-1]
                TEMP_Val *= WeightFaktor
                
                TEMP_Val += HighResM[r_,c_] / correction_factor
                

                TEMP_Val2 = HighResM[r_-1,c_-1]
                TEMP_Val2 += HighResM[r_+1,c_+1]
                TEMP_Val2 += HighResM[r_-1,c_+1]
                TEMP_Val2 += HighResM[r_+1,c_-1]
                TEMP_Val2 *= WeightFaktor2
                
                
                HighResM_new[r_,c_] = TEMP_Val  + TEMP_Val2

        
           
        LowResSumNew[:, :] = CoreLoopSumLowRes(HighResM_new, 
                        ResolutionFactor)
        print (np.sum(LowResSumNew))
        #with nogil, parallel():
        if 1==1:
            for r_ in range(rLow):
                rHighBase = r_ * ResolutionFactor
                for c_ in range(cLow):
                    cHighBase = c_ * ResolutionFactor
                    change_factor_ = (1 + LowResSumOrig[r_, c_]) / (1 + LowResSumNew[r_, c_])

    
                    for rH2 in range(ResolutionFactor):
                        rHigh = rHighBase + rH2
                        for cH2 in range(ResolutionFactor):
                            cHigh = cHighBase + cH2

                            HighResM[rHigh, cHigh] = HighResM_new[rHigh, cHigh] * change_factor_
                            """except:
                                pass
                                
                                print(LowResM.shape[0])
                                print(LowResM.shape[1])
                                print(HighResM.shape[0])
                                print(HighResM.shape[1])
                                print "....."
                                print(rLow)
                                print(cLow)
                                print(rHigh)
                                print(cHigh)
                                print "....."
                                print LowResM[rLow, cLow]
                                print HighResM[rHigh, cHigh]
                            """
        #HighResM[:,:] = HighResM_new
        print ("   LoopTime: %4.2f sec" %(time.time() - st))

        

    return HighResM
    """
    correction_factor = 1 + 4 * WeightFaktor * (1 + 1/ 1.41)
    for i in range(NumberOfLoops):
        HighResM_new = np.zeros_like(HighResM)
        HighResM_new[:,:] = HighResM
        HighResM_new[1:,1:] += WeightFaktor / 1.41 * HighResM[:-1,:-1]
        HighResM_new[:-1,:-1] += WeightFaktor / 1.41 * HighResM[1:,1:]
        HighResM_new[:-1,1:] += WeightFaktor / 1.41 * HighResM[1:,:-1]
        HighResM_new[1:,:-1] += WeightFaktor / 1.41 * HighResM[-1:,1:]
        
        HighResM_new[1:,:] += WeightFaktor * HighResM[:-1,:]
        HighResM_new[:-1,:] += WeightFaktor * HighResM[1:,:]
        HighResM_new[:,1:] += WeightFaktor * HighResM[:,:-1]
        HighResM_new[:,:-1] += WeightFaktor * HighResM[:,1:]
        HighResM_new /= correction_factor
        HighResM = HighResM_new
        
        (LowResSumNew) = CoreLoopSumLowRes(HighResM, 
                        ResolutionFactor)
        
        change_factor = (1 + LowResSumOrig) / (1 + LowResSumNew)
        
        r = HighResM.shape[0]
        c = HighResM.shape[1]
    
        idxM_x_res = ((np.floor(np.arange(r) / ResolutionFactor))[:, np.newaxis] * np.ones(c)).astype("uint32")
        idxM_y_res = (np.ones((r, 1)) *  np.floor(np.arange(c) / ResolutionFactor)).astype("uint32")
    
        HighResM *= change_factor[idxM_x_res, idxM_y_res]
        (LowResSumNew) = CoreLoopSumLowRes(HighResM, 
                        ResolutionFactor)
        
        #print ("-----")
        #print (np.sum(HighResM))
        #print (np.sum(LowResSumNew))
        
    return HighResM
    """
    
def CalcLowResSum(HighResM,
            ResolutionFactor):
    
    
    HighResM = convert_vector(HighResM, DTYPE2)
    ResolutionFactor = convert_vector(ResolutionFactor, DTYPE1)
    
    

    (LowResSum) = CoreLoopSumLowRes(HighResM, 
                        ResolutionFactor)

    return (LowResSum )                    
"""
@cython.wraparound(False)
@cython.boundscheck(False)                             
def CoreLoop(np.ndarray[DTYPE2_t, ndim=2] HighResM,
                             DTYPE1_t ResolutionFactor):
"""   



def CoreLoopSumLowRes(HighResM,
               ResolutionFactor):
  
    """
    cdef DTYPE1_t m
    cdef DTYPE1_t n
    cdef DTYPE1_t mLow
    cdef DTYPE1_t nLow
    """
    r = HighResM.shape[0]
    c = HighResM.shape[1]
    
    rLow = int(np.ceil(r/ ResolutionFactor))
    cLow = int(np.ceil(c/ ResolutionFactor))
    #LowResSum = np.zeros((np.ceil(r/ ResolutionFactor), np.ceil(c/ ResolutionFactor)), dtype= DTYPE2)
    LowResSum = np.zeros((rLow, cLow), dtype= DTYPE2)
    


    
    for rL in range(rLow):
        #mLow = DTYPE1(m / ResolutionFactor)
        rHighBase = rL * ResolutionFactor
        for cL in range(cLow):
            cHighBase = cL * ResolutionFactor
            for rH2 in range(ResolutionFactor):
                rHigh = rHighBase + rH2
                for cH2 in range(ResolutionFactor):
                    cHigh = cHighBase + cH2
                    #nLow = DTYPE1(n / ResolutionFactor)
                    #nLow = (n / ResolutionFactor)
                    try:
                        LowResSum[rL, cL] += HighResM[rHigh, cHigh]
                    except:
                        print(LowResSum.shape[0])
                        print(LowResSum.shape[1])
                        print(HighResM.shape[0])
                        print(HighResM.shape[1])
                        print(".....")
                        print(rL)
                        print(cL)
                        print(rHigh)
                        print(cHigh)
                        print(".....")
                        print(LowResSum[rL, cL])
                        print(HighResM[rHigh, cHigh])
                        
                        
    return LowResSum

    
def CalcHighRes(LowResM,
            ResolutionFactor):
    
    
    LowResM = convert_vector(LowResM, DTYPE2)
    ResolutionFactor = convert_vector(ResolutionFactor, DTYPE1)

    (HighResM) = CoreLoopHighRes(LowResM, 
                        ResolutionFactor)

    return (HighResM ) 

"""
@cython.wraparound(False)
@cython.boundscheck(False)  
"""
def CoreLoopHighRes(LowResM,
               ResolutionFactor):  
    
    
    
    rLow = LowResM.shape[0]
    cLow = LowResM.shape[1]
    
    r = rLow * ResolutionFactor
    c = cLow * ResolutionFactor
    
    
    HighResM = np.zeros((r, c), dtype= DTYPE2)
    

    for rL in range(rLow):
        #mLow = DTYPE1(m / ResolutionFactor)
        rHighBase = rL * ResolutionFactor
        for cL in range(cLow):
            cHighBase = cL * ResolutionFactor
            for rH2 in range(ResolutionFactor):
                rHigh = rHighBase + rH2
                for cH2 in range(ResolutionFactor):
                    cHigh = cHighBase + cH2
                    #nLow = DTYPE1(n / ResolutionFactor)
                    #nLow = (n / ResolutionFactor)
                    try:
                        HighResM[rHigh, cHigh] = LowResM[rL, cL]
                    except:
                        print(LowResM.shape[0])
                        print(LowResM.shape[1])
                        print(HighResM.shape[0])
                        print(HighResM.shape[1])
                        print(".....")
                        print(rLow)
                        print(cLow)
                        print(rHigh)
                        print(cHigh)
                        print(".....")
                        print(LowResM[rL, cL])
                        print(HighResM[rHigh, cHigh])
                        
                        
    return HighResM  
        
def FillWithAverage(HighResM,
            ResolutionFactor=10):
    
    
    HighResM = convert_vector(HighResM, DTYPE2)
    ResolutionFactor = convert_vector(ResolutionFactor, DTYPE1)

    (HighResM) = CoreLoopFillWithAverage(HighResM, 
                        ResolutionFactor)

    return (HighResM ) 

"""
@cython.wraparound(False)
@cython.boundscheck(False)  
"""
def CoreLoopFillWithAverage(HighResM,
               ResolutionFactor):  
    
    
    
    rHighOrig = HighResM.shape[0]
    cHighOrig = HighResM.shape[1]
    
    rLow1 = np.ceil(rHighOrig / ResolutionFactor).astype(int)
    cLow1 = np.ceil(cHighOrig / ResolutionFactor).astype(int)
    
    rLow2 = np.ceil(rHighOrig / (10*ResolutionFactor)).astype(int)
    cLow2 = np.ceil(cHighOrig / (10*ResolutionFactor)).astype(int)
    
    rLow3 = np.ceil(rHighOrig / (100*ResolutionFactor)).astype(int)
    cLow3 = np.ceil(cHighOrig / (100*ResolutionFactor)).astype(int)
    
    rLow4 = np.ceil(rHighOrig / (500*ResolutionFactor)).astype(int)
    cLow4 = np.ceil(cHighOrig / (500*ResolutionFactor)).astype(int)

    
    LowResM1 = np.zeros((rLow1, cLow1), dtype= DTYPE2)
    LowResM2 = np.zeros((rLow2, cLow2), dtype= DTYPE2) 
    LowResM3 = np.zeros((rLow3, cLow3), dtype= DTYPE2)    
    LowResM4 = np.zeros((rLow4, cLow4), dtype= DTYPE2)
       
    LowResMCounter1 = np.zeros((rLow1, cLow1), dtype= DTYPE2) + 10 **-4
    LowResMCounter2 = np.zeros((rLow2, cLow2), dtype= DTYPE2) + 10 **-4
    LowResMCounter3 = np.zeros((rLow3, cLow3), dtype= DTYPE2) + 10 **-4
    LowResMCounter4 = np.zeros((rLow4, cLow4), dtype= DTYPE2) + 10 **-4

    TotalA = 0
    TotalA_counter = 10 **-4
               
    for rH in range(rHighOrig):
        #mLow = DTYPE1(m / ResolutionFactor)
        rL1 = int(rH / ResolutionFactor)
        rL2 = int(rH / ResolutionFactor / 10)
        rL3 = int(rH / ResolutionFactor / 100)
        rL4 = int(rH / ResolutionFactor / 500)
        for cH in range(cHighOrig):
            cL1 = int(cH / ResolutionFactor)
            cL2 = int(cH / ResolutionFactor / 10)
            cL3 = int(cH / ResolutionFactor / 100)
            cL4 = int(cH / ResolutionFactor / 500)
            val = HighResM[rH, cH]
            if val > 0:
                LowResM1[rL1, cL1] += val
                LowResM2[rL2, cL2] += val
                LowResM3[rL3, cL3] += val
                LowResM4[rL4, cL4] += val
                TotalA += val
                
                LowResMCounter1[rL1, cL1] += 1 
                LowResMCounter2[rL2, cL2] += 1 
                LowResMCounter3[rL3, cL3] += 1
                LowResMCounter4[rL4, cL4] += 1 
                TotalA_counter += 1
    
    for rL1 in range(rLow1):
        for cL1 in range(cLow1):
            LowResM1[rL1, cL1] /= LowResMCounter1[rL1, cL1]
    for rL1 in range(rLow2):
        for cL1 in range(cLow2):
            LowResM2[rL1, cL1] /= LowResMCounter2[rL1, cL1]
    for rL1 in range(rLow3):
        for cL1 in range(cLow3):
            LowResM3[rL1, cL1] /= LowResMCounter3[rL1, cL1]
    for rL1 in range(rLow4):
        for cL1 in range(cLow4):
            LowResM4[rL1, cL1] /= LowResMCounter4[rL1, cL1]  
    
    TotalA /= TotalA_counter
    
    for rH in range(rHighOrig):
        #mLow = DTYPE1(m / ResolutionFactor)
        rL1 = int(rH / ResolutionFactor)
        rL2 = int(rH / ResolutionFactor / 10)
        rL3 = int(rH / ResolutionFactor / 100)
        rL4 = int(rH / ResolutionFactor / 500)
        for cH in range(cHighOrig):
            val = HighResM[rH, cH]
            if val == 0:
                cL1 = int(cH / ResolutionFactor)
                cL2 = int(cH / ResolutionFactor / 10)
                cL3 = int(cH / ResolutionFactor / 100)
                cL4 = int(cH / ResolutionFactor / 500)
                val1 = LowResM1[rL1, cL1]
                val2 = LowResM2[rL2, cL2]
                val3 = LowResM3[rL3, cL3]
                val4 = LowResM4[rL4, cL4]
                if val1 > 0: 
                    HighResM[rH, cH] = (1.5 * val1 + val2 + val3 +val4) / 4.5
                elif val2 > 0:
                    HighResM[rH, cH] = (1.5 * val2 + val3 +val4) / 3.5
                elif val3 > 0:
                    HighResM[rH, cH] = (val3 +val4 + 0.5 * TotalA) / 2.5
                elif val4 > 0:
                    HighResM[rH, cH] = (val4 + 0.5 * TotalA) / 1.5
                else:
                    HighResM[rH, cH] = TotalA

    return HighResM  