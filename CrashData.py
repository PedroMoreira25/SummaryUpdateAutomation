from AWS.AWS import getResultQuery, exeQuery, CrashData
from pprint import pprint

result = (exeQuery('129642a0-e2e5-46f7-8288-4837a2291f8c'))

pprint(result)
print("\n")
print("\n")

start = 0
end = 0 
while start < len(result):
    end = end + 5
    pprint(result[start:end])
    start = end 
    print("\n")