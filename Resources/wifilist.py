from subprocess import check_output

scanoutput = check_output(["iwlist", "wlan0", "scan"])

ssid = "WiFi not found"

for line in scanoutput.split():
  line = line.decode("utf-8")
  if line[:5]  == "ESSID":
    ssid = line.split('"')[1]

print (ssid)