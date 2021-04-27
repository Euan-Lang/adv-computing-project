#********************************************Used to test inputbox**************************************
#from InputBox import CreateInputBox
#title = 'data reader'
#message = 'please enter user data'
#inputdata = CreateInputBox(title , message , 400 , 300 )
#print(inputdata)

#*******************************************used to test max function************************************
#from maxFunction import findMaxDict,findMaxList
#listdata = [1,3,5,7,9,2,110,4,899967,55543]
#maxpos = findMaxList(listdata)
#print('the max value is ' + str(listdata[maxpos]) + ' at entry '+ str(maxpos+1) + ' or position '+str(maxpos) +' in the list' )
# dictdata = {0:33,1:44,2:31}
#maxposdict = findMaxDict(dictdata)
#print('the max value is ' + str(dictdata[maxposdict]) + ' at entry '+ str(maxposdict+1) + ' or position/key '+str(maxposdict) +' in the dictionary' )

#*******************************************used to test msgBox************************************
from MsgBox import createMsgBox
err = "test"
createMsgBox(err,"connection error")