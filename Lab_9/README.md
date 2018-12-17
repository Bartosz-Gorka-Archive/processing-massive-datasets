# Processing massive datasets
```bash
factor = 8;
numberOfHashFunctions = 1;
numberOfElements = 100_000;
valueRange = 100_000_000;

TP =  99951	TPR = 0,9995
TN = 88237875	TNR = 0,8833
FN =      0	FNR = 0,0000
FP = 11662174	FPR = 0,1167
Expected FPR = 0,1175
```

```bash
factor = 20;
numberOfHashFunctions = 5;
numberOfElements = 100_000;
valueRange = 100_000_000;

TP =  99951	TPR = 0,9995
TN = 99847758	TNR = 0,9995
FN =      0	FNR = 0,0000
FP =  52291	FPR = 0,0005
Expected FPR = 0,0005
```

