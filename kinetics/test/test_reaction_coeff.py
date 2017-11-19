
import sys
sys.path.append('src')

import chemkin

#Function: Constant 
## testing for correct values 
def test_constant_value():
     assert(chemkin.ChemKin.reaction_coeff.constant(10**4) == 10**4)

def test_constant_value_decimals():
     assert(chemkin.ChemKin.reaction_coeff.constant(4.734) == 4.734)
    
## testing for errors
###type
def test_constant_type():
    try:
        chemkin.ChemKin.reaction_coeff.constant("Cool")
    except TypeError as err:
        assert(type(err) == TypeError)

###value
def test_constant_value_negative():
    try:
        chemkin.ChemKin.reaction_coeff.constant(-5)
    except ValueError as err:
        assert(type(err) == ValueError)

#except Exception as err:
#assert type(err) == TypeError, "Bad products should raise a TypeError."

#Function: Arrhenius reaction rate coefficient
## testing for correct values 
def test_Arrhenius_value():
     assert(chemkin.ChemKin.reaction_coeff.arr(10**2, A=10**7, E=10**3) == 3003549.0889639612)

def test_Arrhenius_value_double_check():
     assert(chemkin.ChemKin.reaction_coeff.arr(10**4, A=10**3, E=10**4) == 886.67297841210575)
    
## testing for errors
###argument number
def test_Arrhenius_argument_number():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**4, 10**2, A=10**7, E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)
        
###type
def test_Arrhenius_type_A():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**2, A=('panama'), E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)

def test_Arrhenius_type_E():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**3, A=10**7,E=('panama'))
    except TypeError as err:
        assert(type(err) == TypeError)

def test_Arrhenius_type_T():
    try:
        chemkin.ChemKin.reaction_coeff.arr(('panama'), A=10**7, E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)
        
###value
def test_Arrhenius_value_negative_A():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**2, A=-10**7, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_value_negative_E():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**2, A=10**7, E=-10**3)
    except ValueError as err:
        assert(type(err) == ValueError)
        
def test_Arrhenius_value_negative_T():
    try:
        chemkin.ChemKin.reaction_coeff.arr(-10**2, A=10**7, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)
        
###flow
def test_Arrhenius_flow_A():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**2, A=float('inf'), E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_flow_E():
    try:
        chemkin.ChemKin.reaction_coeff.arr(10**2, A=10**3, E=float('inf'))
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_flow_T():
    try:
        chemkin.ChemKin.reaction_coeff.arr(float('inf'), A=10**2, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)
        


#Function: modified Arrhenius reaction rate coefficient 
## testing for correct values 
def test_Arrhenius_modified_value():
     assert(chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=0.5, E=10**3) == 30035490.889639609)

def test_Arrhenius_modified_value_double_check():
     assert(chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**3, b=0.2, E=10**3) == 754.45742029415351)
    
## testing for errors
###argument number
def test_Arrhenius_modified_argument_number():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**4, 10**3, A=10**7, b=0.4, E=10**2)
    except TypeError as err:
        assert(type(err) == TypeError)
        
###type
def test_Arrhenius_modified_type_A():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=('panama'), b=0.4, E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)

def test_Arrhenius_modified_type_b():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=('panama'), E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)

def test_Arrhenius_modified_type_E():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=0.4,E=('panama'))
    except TypeError as err:
        assert(type(err) == TypeError)

def test_Arrhenius_modified_type_T():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(('panama'), A=10**7, b=0.4, E=10**3)
    except TypeError as err:
        assert(type(err) == TypeError)
        
#value
def test_Arrhenius_modified_value_negative_A():
    try:  
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=-10**7, b=0.3, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_modified_value_negative_E():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**7, b=0.3, E=-10**3)
    except ValueError as err:
        assert(type(err) == ValueError)
        
def test_Arrhenius_modified_value_negative_T():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(-10**2, A=10**7, b=0.3, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

###flow

def test_Arrhenius_flow_A():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=float('inf'), b=0.3, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_flow_b():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**3, b=float('inf'), E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_flow_E():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(10**2, A=10**3, b=0.3, E=float('inf'))
    except ValueError as err:
        assert(type(err) == ValueError)

def test_Arrhenius_flow_T():
    try:
        chemkin.ChemKin.reaction_coeff.mod_arr(float('inf'), A=10**2, b=0.3, E=10**3)
    except ValueError as err:
        assert(type(err) == ValueError)