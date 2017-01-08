import os
import os.path

os.popen("curl -H \"Accept: application/json\" -X GET http://192.168.1.218/api/DcZzpVuSu-QvslbqfaBUR3WpqlY7IT4e80LuUrQY/groups  > lights")
cmdout = os.popen("cat lights").read()
print cmdout
group_names = os.popen("cat lights | grep -P -o '\"name\":\".*?\"' | grep -o ':\".*\"' | tr -d '\"' | tr -d ':'").read()
lstate = os.popen("cat lights | grep -o '\"on\":true,\|\"on\":false,' | tr -d '\"on\":' | tr -d ','").read()
os.popen("rm lights")
result_array = group_names.split('\n')
num_groups = len(result_array) - 1
lstate_a = lstate.split('\n')

if not brite:
    print "not brite"
else: 
    print "guess it was brite"
    
