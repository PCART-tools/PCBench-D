def test_RuleSet():
    net = ({add: ({VAR: ({VAR: ({}, [1]), 1: ({}, [0])}, []),
            inc: ({VAR: ({inc: ({VAR: ({}, [2, 3])}, [])}, [])}, [])}, []),
            list: ({VAR: ({}, [5])}, []),
            sum: ({list: ({VAR: ({VAR: ({VAR: ({}, [4])}, [])}, [])}, [])}, [])}, [])
    assert rs._net == net
    assert rs.rules == rules
