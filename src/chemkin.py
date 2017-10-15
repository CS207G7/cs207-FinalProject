import numpy as np

### Part 3 is not included, as we compute progress rate via matrix
def progress_rate_double(v1, v2, x, k):
    """Returns the progress of rate for a system
    
    INPUTS
    =======
    v1: 2 x 3 float vector
    v2: 2 x 3 float vector
    x: 2 x 3 float vector, species concentrations
    k: 2 x 1 float/int list
    
    RETURNS
    ========
    progress rate: 1x2 float array, the progress rates for a reaction of the following form: 
            
            v_a A + v_b B -> v_c C
            v_a A + v_c C -> v_b B + v_c C
    
    EXAMPLES
    =========
    >>> progress_rate_double([[1,2,0],[2,0,2]], [[0,0,2],[0,1,1]], [1,2,1], [10,10])
    array([40, 10])
    """
    try:
        x = np.array(x)
        v1 = np.array(v1)
        v2 = np.array(v2)
        k = np.array(k)
    except TypeError as err:
        raise TypeError("x and v should be either int or float vectors")
    
    if k.any() < 0:
        raise ValueError("reaction constant can't be negative")
    
    return  k * np.prod(x ** v1, axis=1)

import numpy as np

def rr(v1, v2, x, k):
    """Returns the reaction rate for a system
    
    INPUTS
    =======
    v1: 2 x 3 float vector
    v2: 2 x 3 float vector
    x: 2 x 3 float vector, species concentrations
    k: 2 x 1 float/int list
    
    RETURNS
    ========
    reaction rates: 1x3 float array, the reaction rate for each specie
            
    EXAMPLES
    =========
    >>> rr([[1,2,0],[0,0,2]], [[0,0,1],[1,2,0]], [1,2,1], [10,10])
    array([-30, -60,  20])
    """
    try:
        
        x = np.array(x)
        v1 = np.array(v1)
        v2 = np.array(v2)
        k = np.array(k)
        
    except TypeError as err:
        raise TypeError("x and v should be either int or float vectors")
    
    if k.any() < 0:
        raise ValueError("reaction constant can't be negative")
    
    ws = progress_rate_double(v1, v2, x, k)
    rrs = np.sum((v2 - v1) * np.array([ws]).T, axis=0)
    
    return rrs