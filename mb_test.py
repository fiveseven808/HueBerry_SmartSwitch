import authenticate
blah = authenticate.Authenticate()
result = blah.search_for_all_bridges(debug = 1)
print result

ip = result
for each_ip in ip:
    print each_ip
