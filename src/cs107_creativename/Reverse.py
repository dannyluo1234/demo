# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 16:04:57 2021

@author: Danny Luo
"""

import math
from inspect import signature

class Node():
    """
    A Node class that keeps track of the current value and derivative of a
    variable in a function or function set, as well as the pointers to all of
    the Nodes that depend on it (i.e. its "children").
    It should be initiated by calling the class followed by a real number.

    Parameters
    ----------
    val : real number
          The current value of the Node. Has to be defined at instantiation.
    der : real number
          The current derivative of the Node
    children : a list of tuples, each tuple representing a child
               The first value in the tuple is a pointer to the child node, and
               the second value in the pointer is its current partial derivative

    Returns
    ----------
    Node
        Returns a Node class object

    Examples
    ----------
    >>> x = Node(3)
    """
    def __init__(self, val):
        """
        Intialize a Dual class object with an empty list of children and
        no derivative value.
        """
        if isinstance(val, int) or isinstance(val, float):
            self.val = val
            # children will store tuples of form (a,b) where a is a child and b is  
            # this child's partial derivative
            self.children = []
            self.der = None
        else:
            raise TypeError
    
    def get_gradient(self):
        """
        Returns the current derivative of a node. If the dertivative is None,
        update the derivative to a sum of all of its children's partial
        derivatives and return that value.
        """
        if self.der is not None:
            return self.der
        else:
            self.der = sum([child.get_gradient() * partial for child, partial in self.children])
            return self.der

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(self.val + other)
            self.children.append((new_node, 1))
            return new_node
        elif isinstance(other, Node):
            new_node = Node(self.val + other.val)
            self.children.append((new_node, 1))
            other.children.append((new_node, 1))
            return new_node
        else:
            raise TypeError
            
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(self.val * other)
            self.children.append((new_node, other))
            return new_node
        elif isinstance(other, Node):
            new_node = Node(self.val * other.val)
            self.children.append((new_node, other.val))
            other.children.append((new_node, self.val))
            return new_node
        else:
            raise TypeError
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(self.val / other)
            self.children.append((new_node, 1/other))
            return new_node
        elif isinstance(other, Node):
            new_node = Node(self.val / other.val)
            self.children.append((new_node, 1 / other.val))
            other.children.append((new_node, - self.val / (other.val ** 2)))
            return new_node
        else:
            raise TypeError       

    def __rtruediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(other / self.val)
            self.children.append((new_node, - other / (self.val ** 2)))
            return new_node
        else:
            raise TypeError  

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(self.val - other)
            self.children.append((new_node, 1))
            return new_node
        elif isinstance(other, Node):
            new_node = Node(self.val - other.val)
            self.children.append((new_node, 1))
            other.children.append((new_node, -1))
            return new_node
        else:
            raise TypeError
    
    def __rsub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(other - self.val)
            self.children.append((new_node, -1))
            return new_node
        else:
            raise TypeError  
            
    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(self.val ** other)
            self.children.append((new_node, other * self.val ** (other-1)))
            return new_node        
        elif isinstance(other, Node):
            new_node = Node(self.val ** other.val)
            self.children.append((new_node, other.val * self.val ** (other.val-1)))
            other.children.append((new_node, self.val ** other.val * math.log(other.val)))
            return new_node       
        else:
            raise TypeError         
    
    def __rpow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            new_node = Node(other ** self.val)
            self.children.append((new_node, other ** self.val * math.log(other)))
            return new_node 
        else:
            raise TypeError
    
    def __neg__(self):
        return self.__mul__(-1)

    def __lt__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.val < other
        elif isinstance(other, Node):
            return self.val < other.val
        else:
            raise TypeError

    def __gt__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.val > other
        elif isinstance(other, Node):
            return self.val > other.val
        else:
            raise TypeError

    def __le__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.val <= other
        elif isinstance(other, Node):
            return self.val <= other.val
        else:
            raise TypeError    

    def __ge__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.val >= other
        elif isinstance(other, Node):
            return self.val >= other.val
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.val == other.val and self.der == other.der and self.children == other.children
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)            
            

    # using reverse pass to calculate the gradient of specific variables
    def _AutoDiffR(self, variables):
        self.der = 1
        result = []
        for var in variables:
            '''
            try:
                var_grad = var.get_gradient()
                result.append(var_grad)
            except:
                print("Variable Not specified")
                return
            '''
            var_grad = var.get_gradient()
            result.append(var_grad)
        return result

# One dimensional case wher f: R^n to R
def AutoDiffR1D(f, val):
    try:
        dimension = len(signature(f).parameters)
    except:
        raise TypeError("the first argument must be a function")
        
    if dimension != len(val):
        raise Exception("provided value doesn't match the input dimension of f")
    
    variables = [Node(val[i]) for i in range(dimension)]
    result = f(*variables)        
    return result._AutoDiffR(variables)

# General Case, f_list could be a list of functions
def AutoDiffR(f_list, val_list):
    if isinstance(f_list, list):
        results = []
        if len(f_list) != len(val_list):
            raise Exception("function list length doesn't match value list length")
        for f, val in zip(f_list, val_list):
            results.append(AutoDiffR1D(f, val))
        return results
    else:
        return AutoDiffR1D(f_list, val_list)
        

















