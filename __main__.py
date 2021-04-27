from Login import login
from Options import launchOptions
userDetails = login()
if userDetails:
    launchOptions(userDetails)
