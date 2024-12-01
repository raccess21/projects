from project import occurence
from timemodes import in_interval
from datetime import datetime as dt
from files import get_int

#______________project.py_____________________________
def test_occurence():
    assert occurence("", "is") == 0
    assert occurence([], "is") == 0
    assert occurence("IS", "is") == 1
    assert occurence("", [1]) == 0
    assert occurence(" ", "if i may") == 0
    assert occurence("cs50", "This is CS50 and this is CS50's CS50P.") == 2    
    assert occurence("cs50", "This is 'CS50', this is CS50's CS50P.") == 2    
    assert occurence("will", "I will be making a statement tonight. A big WIN!") == 1

#______________timemodes.py_____________________________
def test_in_interval():
    s_date = dt.strptime("2020/01/01", '%Y/%m/%d')
    e_date = dt.strptime("2024/01/20", '%Y/%m/%d')
    
    assert in_interval(1, s_date, e_date) == False
    assert in_interval(dt.strptime("2020/05/05", "%Y/%m/%d"), s_date, e_date) == True
    assert in_interval(dt.strptime("2010/05/05", "%Y/%m/%d"), s_date, e_date) == False
    
    
    
#______________files.py_____________________________

def test_get_int():
    assert get_int([1, 2, 3, 7], 5) == {1, 2, 3}
    assert get_int(['1', '2', '3', '7'], 5) == {1, 2, 3}
    assert get_int(['a', 'b', 'c', 'd'], 5) == set()
    assert get_int([-1, 1, 2, 3, 7.9], 5) == {1, 2, 3}
   

