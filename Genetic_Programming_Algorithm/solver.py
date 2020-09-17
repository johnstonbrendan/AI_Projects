import numpy as np

def solver(boolString):
    boolString = np.array(boolString)
    if len(boolString) == 6: # 6 multi problem
        addressbits = 2
        data_address = boolString[:addressbits] # will get the address bits
        data_address = np.flip(data_address)
        data_address = np.packbits(data_address,bitorder='little')
        # print(f"address: {data_address}")
        # print(f"boolstring[0] = {boolString[0]} : boolString[5] = {boolString[5]}")
        return int(boolString[data_address+addressbits])

    elif len(boolString) == 11: # 11 multi problem
        addressbits = 3
        data_address = boolString[:addressbits] # will get the address bits
        data_address = np.flip(data_address)
        data_address = np.packbits(data_address,bitorder='little')
        # print(f"address: {data_address}")
        # print(f"boolstring[0] = {boolString[0]} : boolString[5] = {boolString[5]}")
        return int(boolString[data_address+addressbits])

    elif len(boolString) == 16: # 16 middle 3 case
        total = np.sum(boolString)
        if total >= 7 and total <= 9:
            return 1
        else:
            return 0
    
    else:
        raise "not proper length"

        
        

if __name__ == "__main__":
    # this is an example for the 6multi problem
    a3 = np.array([1,0,0,1,1,1]) 
    # print (solver(a3))

    # this is an example for the 11multi problem
    a11 = np.array([1,0,1,0,1,2,3,4,5,6,7])
    # print(f'Solver value: {solver(a11)}')

    # this is an example for the 16 middle 3
    a16 = np.array([1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0])
    print(a16[1])
    print(f'solver value: {solver(a16)}')



    