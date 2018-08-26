import numpy as np
import devfx.mathematics as math
from ..distributions import normal, student, chisquare
from ..series import center, dispersion

""" Confidence intervals
"""
class ci(object):
    """================================================================================================
    """
    class mean(object):
        """--------------------------------------------------------------------------------------------
        """ 
        class normal(object):
            def __init__(self, data):       
                self.data = np.asarray(data)

            @property
            def data(self):
                return self.__data
            
            @data.setter   
            def data(self, data):
                self.__data = data


            def two_sided(self, ccoef=95, sigma=None):
                n = self.data.size
                mean = center.mean(self.data)
                alpha = 1.0-ccoef/100.0
                if(sigma is not None): 
                    d = normal().icdf(1.0-alpha/2.0)
                    thetaL = mean-d*sigma/math.sqrrt(n)
                    thetaU = mean+d*sigma/math.sqrrt(n)
                else:
                    d = student(n-1).icdf(1.0-alpha/2.0)
                    S = dispersion.S(self.data)
                    thetaL = mean-d*S/math.sqrrt(n)
                    thetaU = mean+d*S/math.sqrrt(n)
                return (thetaL, thetaU)
                            
            def lower_one_sided(self, ccoef=95, sigma=None):
                n = self.data.size
                mean = center.mean(self.data)
                alpha = 1.0-ccoef/100.0
                if(sigma is not None): 
                    d = normal().icdf(1.0-alpha)
                    thetaL = mean-d*sigma/math.sqrrt(n)
                    thetaU = +math.inf
                else:
                    d = student(n-1).icdf(1.0-alpha)
                    S = dispersion.S(self.data)
                    thetaL = mean-d*S/math.sqrrt(n)
                    thetaU = +math.inf
                return (thetaL, thetaU)
                
            def upper_one_sided(self, ccoef=95, sigma=None):
                n = self.data.size
                mean = center.mean(self.data)
                alpha = 1.0-ccoef/100.0
                if(sigma is not None): 
                    d = normal().icdf(1.0-alpha)
                    thetaL = -math.inf
                    thetaU = mean+d*sigma/math.sqrrt(n)
                else:
                    d = student(n-1).icdf(1.0-alpha)
                    S = dispersion.S(self.data)
                    thetaL = -math.inf
                    thetaU = mean+d*S/math.sqrrt(n)
                return (thetaL, thetaU)
        
        """--------------------------------------------------------------------------------------------
        """
        class unknown(normal):
            def __init__(self, data):
                super().__init__(data)
         

    """================================================================================================
    """         
    class mean_difference(object):
        """--------------------------------------------------------------------------------------------
        """ 
        class normal(object):
            def __init__(self, data1, data2):       
                self.data1 = np.asarray(data1)
                self.data2 = np.asarray(data2)
            
            
            @property 
            def data1(self):
                return self.__data1
            
            @data1.setter   
            def data1(self, data1):
                self.__data1 = data1
        
            @property 
            def data2(self):
                return self.__data2
            
            @data2.setter   
            def data2(self, data2):
                self.__data2 = data2
        
        
            def two_sided(self, ccoef=95, sigmas=None):
                (n1, n2) = (self.data1.size, self.data2.size)
                (mean1, mean2) = (center.mean(self.data1), center.mean(self.data2))
                alpha = 1.0-ccoef/100.0
                if(sigmas is not None):
                    (sigma1, sigma2) = sigmas
                    d = normal().icdf(1.0-alpha/2.0)
                    thetaL = (mean1-mean2)-d*math.sqrrt(sigma1**2/n1+sigma2**2/n2)
                    thetaU = (mean1-mean2)+d*math.sqrrt(sigma1**2/n1+sigma2**2/n2)
                else:
                    (S1, S2) = (dispersion.S(self.data1), dispersion.S(self.data2))
                    n = math.floor((S1**2/n1+S2**2/n2)**2/((1.0/(n1-1))*(S1**2/n1)**2+(1.0/(n2-1))*(S2**2/n2)**2))
                    d = student(n).icdf(1.0-alpha/2.0)
                    thetaL = (mean1-mean2)-d*math.sqrrt(S1**2/n1+S2**2/n2)
                    thetaU = (mean1-mean2)+d*math.sqrrt(S1**2/n1+S2**2/n2)
                return (thetaL, thetaU)
                         
            def lower_one_sided(self, ccoef=95, sigmas=None):           
                (n1, n2) = (self.data1.size, self.data2.size)
                (mean1, mean2) = (center.mean(self.data1), center.mean(self.data2))
                alpha = 1.0-ccoef/100.0
                if(sigmas is not None):
                    (sigma1, sigma2) = sigmas
                    d = normal().icdf(1.0-alpha)
                    thetaL = (mean1-mean2)-d*math.sqrrt(sigma1**2/n1+sigma2**2/n2)
                    thetaU = +math.inf
                else:
                    (S1, S2) = (dispersion.S(self.data1), dispersion.S(self.data2))
                    n = math.floor((S1**2/n1+S2**2/n2)**2/((1.0/(n1-1))*(S1**2/n1)**2+(1.0/(n2-1))*(S2**2/n2)**2))
                    d = student(n).icdf(1.0-alpha)
                    thetaL = (mean1-mean2)-d*math.sqrrt(S1**2/n1+S2**2/n2)
                    thetaU = +math.inf
                return (thetaL, thetaU)
                
            def upper_one_sided(self, ccoef=95, sigmas=None):           
                (n1, n2) = (self.data1.size, self.data2.size)
                (mean1, mean2) = (center.mean(self.data1), center.mean(self.data2))
                alpha = 1.0 - ccoef/100.0
                if(sigmas is not None):
                    (sigma1, sigma2) = sigmas
                    d = normal().icdf(1.0-alpha)
                    thetaL = -math.inf
                    thetaU = (mean1-mean2)+d*math.sqrrt(sigma1**2/n1+sigma2**2/n2)
                else:
                    (S1, S2) = (dispersion.S(self.data1), dispersion.S(self.data2))
                    n = math.floor((S1**2/n1+S2**2/n2)**2/((1.0/(n1-1))*(S1**2/n1)**2+(1.0/(n2-1))*(S2**2/n2)**2))
                    d = student(n).icdf(1.0-alpha)
                    thetaL = -math.inf
                    thetaU = (mean1-mean2)+d*math.sqrrt(S1**2/n1+S2**2/n2)
                return (thetaL, thetaU)
        
        """--------------------------------------------------------------------------------------------
        """ 
        class unknown(normal):
            def __init__(self, data1, data2):       
                super().__init__(data1, data2)


    """================================================================================================
    """      
    class variance(object):
        """--------------------------------------------------------------------------------------------
        """ 
        class normal(object):
            def __init__(self, data):       
                self.data = np.asarray(data)
            
            
            @property 
            def data(self):
                return self.__data
            
            @data.setter   
            def data(self, data):
                self.__data = data
                
            
            def two_sided(self, ccoef=95):
                n = self.data.size
                S2 = dispersion.S2(self.data)
                alpha = 1.0-ccoef/100.0
                dL = chisquare(n-1).icdf(alpha/2.0)
                dU = chisquare(n-1).icdf(1.0-alpha/2.0)
                thetaL = (n-1)*S2/dU
                thetaU = (n-1)*S2/dL
                return (thetaL, thetaU)
                                       
            def lower_one_sided(self, ccoef=95):
                n = self.data.size
                S2 = dispersion.S2(self.data)
                alpha = 1.0-ccoef/100.0
                dU = chisquare(n-1).icdf(1.0-alpha)
                thetaL = (n-1)*S2/dU
                thetaU = +math.inf
                return (thetaL, thetaU)
                
            def upper_one_sided(self, ccoef=95):
                n = self.data.size
                S2 = dispersion.S2(self.data)
                alpha = 1.0-ccoef/100.0
                dL = chisquare(n-1).icdf(alpha)
                thetaL = math.zero
                thetaU = (n-1)*S2/dL
                return (thetaL, thetaU)
                
                    
    """================================================================================================
    """  
    class variance_ratio(object):
        pass
