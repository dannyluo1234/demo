# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 17:47:39 2021

@author: Danny Luo
"""

import math
import numpy as np

class Dual():
    def __init__(self, value, direction=1):
        if (isinstance(value, int) or isinstance(value, float)) and (isinstance(direction, int) or isinstance(direction, float)):
            self.val = value
            self.der = direction
        else:
            raise TypeError
        
    def __add__(self, other):
        if isinstance(other, Dual) :
            return Dual(self.val + other.val, self.der + other.der)
        elif isinstance(other, float) or isinstance(other, int):
            return Dual(self.val + other, self.der)
        else:
            raise TypeError
            
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.val * other, self.der * other)
        elif isinstance(other, Dual):
            return Dual(self.val * other.val, self.der * other.val + self.val * other.der)
        else:
            raise TypeError
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.val / other, self.der / other)        
        elif isinstance(other, Dual):
            return Dual(self.val / other.val, (self.der * other.val - self.val * other.der)/(other.val**2))
        else:
            raise TypeError        
    
    def __rtruediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(other/self.val, -self.der * other /(self.val ** 2))     
        else:
            raise TypeError      
            
    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.val - other, self.der)   
        elif isinstance(other, Dual):
            return Dual(self.val - other.val, self.der - other.der)
        else:
            raise TypeError 
    
    def __rsub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(other-self.val, -self.der )     
        else:
            raise TypeError     
            
    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.val ** other, other * self.val ** (other-1) * self.der)   
        elif isinstance(other, Dual):
            return Dual(self.val ** other.val, self.val ** other.val * (other.der * math.log(self.val) + other.val / self.val * self.der))
        else:
            raise TypeError         
    
    def __rpow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(other ** self.val, self.der * math.log(other) )     
        
def sin(other):
    if isinstance(other, float) or isinstance(other, int):
        return math.sin(other)  
    elif isinstance(other, Dual):
        return Dual(math.sin(other.val), math.cos(other.val) * other.der)
    else:
        raise TypeError  

def cos(other):
    if isinstance(other, float) or isinstance(other, int):
        return math.cos(other)  
    elif isinstance(other, Dual):
        return Dual(math.cos(other.val), -math.sin(other.val) * other.der)
    else:
        raise TypeError          

def tan(other):
    if isinstance(other, float) or isinstance(other, int):
        return math.tan(other)  
    elif isinstance(other, Dual):
        return Dual(math.tan(other.val), 1 / (math.cos(other.val) ** 2) * other.der)
    else:
        raise TypeError  
        
def arcsin(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arcsin(other)  
    elif isinstance(other, Dual):
        return Dual(np.arcsin(other.val), (1 / (1-other.val**2)**0.5) * other.der)
    else:
        raise TypeError  
        
def arccos(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arccos(other)  
    elif isinstance(other, Dual):
        return Dual(np.arccos(other.val), -(1 / (1-other.val**2)**0.5) * other.der)
    else:
        raise TypeError  
        
def arctan(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arctan(other)  
    elif isinstance(other, Dual):
        return Dual(np.arctan(other.val), (1 / (1+other.val**2)) * other.der)
    else:
        raise TypeError  
        
def sinh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.sinh(other)  
    elif isinstance(other, Dual):
        return Dual(np.sinh(other.val), np.cosh(other.val) * other.der)
    else:
        raise TypeError
        
def cosh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.cosh(other)  
    elif isinstance(other, Dual):
        return Dual(np.cosh(other.val), np.sinh(other.val) * other.der)
    else:
        raise TypeError
        
def tanh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.tanh(other)  
    elif isinstance(other, Dual):
        return Dual(np.tanh(other.val), (1 / np.cosh(other.val)**2) * other.der)
    else:
        raise TypeError
    
def arcsinh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arcsinh(other)  
    elif isinstance(other, Dual):
        return Dual(np.arcsinh(other.val), (1 / (other.val**2 + 1)**0.5) * other.der)
    else:
        raise TypeError

def arccosh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arccosh(other)  
    elif isinstance(other, Dual):
        return Dual(np.arccosh(other.val), (1 / (other.val**2 - 1)**0.5) * other.der)
    else:
        raise TypeError
    
def arctanh(other):
    if isinstance(other, float) or isinstance(other, int):
        return np.arctanh(other)  
    elif isinstance(other, Dual):
        return Dual(np.arctanh(other.val), (1 / (1-other.val**2)) * other.der)
    else:
        raise TypeError
        
def exp(other):
    if isinstance(other, float) or isinstance(other, int):
        return math.exp(other)  
    elif isinstance(other, Dual):
        return Dual(math.exp(other.val), math.exp(other.val) * other.der)
    else:
        raise TypeError             

# To get the gradient, we need to set different seed for different coordinate and calculate the forward mode for n times where n is the dimension
def get_gradient(f,dimension,value):
    gradient = []

    # For loop over dimension, each calculating one coordinate of the gradient
    for i in range(dimension):

        # Initialize the Dual numbers with the specific seed, the seed should have 1 at the current dimension and 0 in other dimension.
        Dual_list = []

        # Loop over all the variables to initialize it
        for j in range(dimension):
            # This is the only variable that has 1 as the self.der
            if i == j:
                Dual_list.append(Dual(value[j], 1))
            # All other Dual variables should have 0 as the self.der as specified by the seed
            else:
                Dual_list.append(Dual(value[j], 0))

        # Perform Forward Mode
        function = f(*Dual_list)

        # Attach this coordinate to the final result
        gradient.append(function.der)
    return gradient
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        