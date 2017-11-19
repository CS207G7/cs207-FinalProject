import sys
sys.path.append('src')
import chemkin

#Function: Cp_over_R

## testing for correct values
def test_Cp_over_R_result():
    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291],/
                     [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
    Tmax = 3500.000
    compare = np.array([2.4999999988594293, 4.9171811841624997])
    output = thermochem.Cp_over_R(H_O2,Tmax)
    assert np.equal(output, compare).all() == 0, 'Expected outcome'

def test_Cp_over_R_bad_result():
    H_O2 = np.array([[2.50000001, -2.30842973e-11, 1.61561948e-14, -4.73515235e-18, 4.98197357e-22, 25473.6599, -0.44668291],/
                     [3.28253784, 0.00148308754, -7.57966669e-07, 2.09470555e-10, -2.16717794e-14, -1088.45772, 5.4532312]]).T
    Tmax = 3500.000
    compare = np.array([2.6, 4.7])
    output = thermochem.Cp_over_R(H_O2,Tmax)
    assert np.equal(output, compare).all() == 1, 'Unexpected outcome'

## testing for argument number
def test_reaction_Cp_over_R_argument_number():
    try:
        chemkin.Reaction.Cp_over_R(10**4, 10**2, 10**7)
    except TypeError as err:
        assert type(err) == TypeError, 'Wrong args number'

## testing for type errors
def test_reaction_Cp_over_R_T_text():
    try:
        chemkin.Reaction.Cp_over_R(('panama'))
    except Exception as err:
        assert type(err) == TypeError, 'Bad args format'

def test_reaction_Cp_over_R_T_negative():
    try:
        chemkin.Reaction.Cp_over_R(-10**2)
    except Exception as err:
        assert type(err) == TypeError, 'Bad args format'

def test_reaction_Cp_over_R_T_flow():
    try:
        chemkin.Reaction.Cp_over_R(float('inf'))
    except Exception as err:
        assert type(err) == TypeError, 'Bad args format'
