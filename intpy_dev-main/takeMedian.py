import sys
import statistics


lista = []
for i in range(1,len(sys.argv)):
    print(sys.argv[i])
    lista.append((float) (sys.argv[i]))
print(statistics.median(lista))
