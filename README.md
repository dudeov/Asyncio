# Asyncio

```
alex.chuvakov@DE1T3NNETHOP01:~/scripts$ python3 ssh_v5_async.py -d cfw -f test -c 'sh ver, sh ver'      
Username: cne
Password for cne: 
Connected to DE3_CFW
Connected to GB1_CFW
Connected to GB3_CFW
Connected to DE1_CFW
Ran the command sh ver on DE3_CFW
Ran the command sh ver on GB1_CFW
Ran the command sh ver on GB3_CFW
Ran the command  sh ver on DE3_CFW
Ran the command  sh ver on GB1_CFW
Ran the command  sh ver on GB3_CFW
Connected to NY1_CFW
...
--- 4.36 seconds ---
```

Many times faster that the old serial ```ssh-v4.py```


```

alex.chuvakov@DE1T3NNETHOP01:~/scripts$ python3 ssh-v4.py -d cfw -f test -c 'sh ver, sh ver'         
Username: cne
Password for cne: 
test_AU1_CFW.txt
trying...
Connected to AU1_CFW
sh ver
 sh ver
test_CA1_CFW.txt
trying...
Connected to CA1_CFW
sh ver
 sh ver
test_CA2_CFW.txt
trying...
Connected to CA2_CFW
sh ver
 sh ver
test_CA3_CFW.txt
...
--- 48.40 seconds ---

```
