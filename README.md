Git workflow
          +---------+
          |   main  |
          +---------+
              |       
          +---------+        Merge
          | develop | <--------------+
          +---------+                |
            /       \                |
           /         \               |
          /           \              |
+----------------+  +----------------+  
| feature/login  |  | feature/signup |
+----------------+  +----------------+ 


for autoscaller
#run monitor.py
pyhton monitor.py

#For load testing
stress-ng --cpu 4 --timeout 300s --cpu-load 80

