# How to use it
1. Download modules
- For Mac
```
pip3 install requests
pip3 install email==6.0.0a1
pip3 install secure-smtplib
```
- For Windows
```
pip install requests
pip install email==6.0.0a1
pip install secure-smtplib
```
2. Run python script
- For Windows
```
directory_of_the_script>python email.py
```
- For Mac
```
directory_of_the_script$ python3 email.py
```
# Cautions
1. If you want to send a piece of email every day at the same time, unfortunatelly, the script will stop working once you close the console window since cloud services are not used in this case. However, because AWS cloud service is free for small projects, you can always do it yourself.
