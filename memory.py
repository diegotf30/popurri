import popurri_tokens

MEM_DEFAULT = 160000


class Memory():

    # Direcciones:

    # global int : 0 - 9999
    # global float : 10000 - 19999
    # global string : 20000 - 29999
    # global bool : 30000 - 39999

    # local int : 40000 - 49999
    # local float : 50000 - 59999
    # local string : 60000 - 69999
    # local bool : 70000 - 79999

    # temp int : 80000 - 89999
    # temp float : 90000 - 99999
    # temp string : 100000 - 109999
    # temp bool : 110000 - 119999

    # cte int : 120000 - 129999
    # cte float : 130000 - 139999
    # cte string : 140000 - 149999
    # cte bool : 150000 - 159999

    def __init__(self):
        self.global_index = 0
        self.local_index = 40000
        self.temp_index = 80000
        self.cte_index = 120000
