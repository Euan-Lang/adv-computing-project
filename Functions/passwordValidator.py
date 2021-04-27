def validatePassword(unvalidatedPass):
    val = True
      
    if len(unvalidatedPass) < 8:   
        val = False     
    elif not any(char.isdigit() for char in unvalidatedPass): 
        val = False      
    elif not any(char.isupper() for char in unvalidatedPass): 
        val = False
    elif not any(char.islower() for char in unvalidatedPass): 
        print('Password should have at least one lowercase letter') 
        val = False 
    return val 