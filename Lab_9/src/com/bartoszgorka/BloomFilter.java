package com.bartoszgorka;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashSet;
import java.util.Random;

public class BloomFilter {
    private int filterSize = 0;
    private int numberOfElements = 0;
    private int numberOfHashFunctions = 0;
    private int prime;
    private BitSet vector;
    private ArrayList<HashFunction> functions = new ArrayList<>();

    private BloomFilter(int filterSize, int numberOfHashFunctions, int numberOfElements) {
        this.filterSize = filterSize;
        this.numberOfHashFunctions = numberOfHashFunctions;
        this.numberOfElements = numberOfElements;

        // Set BitSet vector
        this.vector = new BitSet(filterSize);

        // Calculate prime number and store it in object
        this.prime = this.findPrimeNumber();

        // Run generator hash functions
        this.prepareHashFunctions();
    }

    private int findPrimeNumber() {
        BigInteger value = new BigInteger(String.valueOf(this.filterSize));
        return value.nextProbablePrime().intValue();
    }

    private void prepareHashFunctions() {
        Random rand = new Random(0);

        for(int i = 1; i <= this.numberOfHashFunctions; ++i) {
            int a = rand.nextInt(this.prime - 1) + 1;
            int b = rand.nextInt(this.prime);
            HashFunction hashFunction = new HashFunction(a, b);
            this.functions.add(hashFunction);
        }
    }

    private int[] generateHash(int value) {
        int pointer = 0;
        int[] result = new int[this.numberOfHashFunctions];

        for(HashFunction function : this.functions) {
            result[pointer] = function.hash(value, this.prime) % this.filterSize;
            ++pointer;
        }

        return result;
    }

    private void add(int value) {
        int[] positions = generateHash(value);
        for(int position : positions) {
            this.vector.set(position);
        }
    }

    private Boolean contains(int value) {
        int[] positions = generateHash(value);
        boolean found = true;

        for(int position : positions) {
            // When found position with 0 (false) - break loop because value not exist in BloomFilter
            if (!this.vector.get(position)) {
                found = false;
                break;
            }
        }

        return found;
    }

    private double calculateExpectedFP() {
        return Math.pow(1 -
                Math.exp(-this.numberOfHashFunctions * (double)this.numberOfElements / this.filterSize),
                this.numberOfHashFunctions);
    }

    private void generateStats(int valueRange, HashSet<Integer> set) {
        int TP = 0, FP = 0, TN = 0, FN = 0, key;

        for (int i = 0; i < valueRange; i++) {
            key = i;
            Boolean containsBF = this.contains(key);
            Boolean containsHS = set.contains(key);

            if (containsBF && containsHS) {
                TP++;
            } else if (!containsBF && !containsHS) {
                TN++;
            } else if (!containsBF) {
                FN++;
            } else {
                FP++;
            }
        }

        System.out.println("TP = " + String.format("%6d", TP) + "\tTPR = "
                + String.format("%1.4f", (double) TP / (double) numberOfElements));
        System.out.println("TN = " + String.format("%6d", TN) + "\tTNR = "
                + String.format("%1.4f", (double) TN / (double) (valueRange - numberOfElements)));
        System.out.println("FN = " + String.format("%6d", FN) + "\tFNR = "
                + String.format("%1.4f", (double) FN / (double) (numberOfElements)));
        System.out.println("FP = " + String.format("%6d", FP) + "\tFPR = "
                + String.format("%1.4f", (double) FP / (double) (valueRange - numberOfElements)));
        System.out.println("Expected FPR = " + String.format("%1.4f", this.calculateExpectedFP()));
    }

    public static void main(String[] args) {
        double factor = 20;
        int numberOfHashFunctions = 5;
        int numberOfElements = 100_000;
        int valueRange = 100_000_000;

        int filterSize = (int) Math.round(factor * numberOfElements);

        Random random = new Random(0);
        BloomFilter bf = new BloomFilter(filterSize, numberOfHashFunctions, numberOfElements);
        HashSet<Integer> set = new HashSet<>(numberOfElements);

        // Generate random keys to store in BloomFilter
        for(int i = 0; i <= numberOfElements; ++i) {
            set.add(random.nextInt(valueRange));
        }

        // Add all generated items to bitmap
        for (int item : set) {
            bf.add(item);
        }

        // Calculate stats and verify implementation
        bf.generateStats(valueRange, set);
    }
}
