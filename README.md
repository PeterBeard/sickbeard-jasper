# sickbeard-jasper
A Jasper module for interacting with Sick Beard

# Configuration
Create a Sick Beard section in ~/.jasper/profile.yml that looks like this:
```
sickbeard:
    host: 192.168.1.100
    port: 8080
    api_key: 00000000000000000000000000000000
```

Make sure the API is enabled on the Sick Beard configuration page and that Jasper can reach the machine running Sick Beard and everything should work fine.
