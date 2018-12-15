package com.bartoszgorka;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashSet;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

// TODO calculate stats and verify results

public class BloomFilter {
    private int size = 0;
    private int n = 0;
    private int k = 0;
    private int prime;
    private BitSet vector;
    private ArrayList<HashFunction> functions = new ArrayList<>();

    private BloomFilter(int size, int k, int n) {
        this.size = size;
        this.k = k;
        this.n = n;

        // Set bitset
        this.vector = new BitSet(size);

        // Calculate prime number and store it in object
        this.prime = this.primeNumber();

        // Run generator hash functions
        this.prepareHashFunctions();
    }

    private int primeNumber() {
        BigInteger value = new BigInteger(String.valueOf(this.size));
        return value.nextProbablePrime().intValue();
    }

    private void prepareHashFunctions() {
        for(int i = 1; i <= this.k; ++i) {
            long a = ThreadLocalRandom.current().nextInt(1, this.prime);
            long b = ThreadLocalRandom.current().nextInt(0, this.prime);
            HashFunction hashFunction = new HashFunction(a, b);
            this.functions.add(hashFunction);
        }
    }

    private int[] generateHash(int value) {
        int pointer = 0;
        int[] result = new int[this.k];

        for(HashFunction function : this.functions) {
            result[pointer] = (int)(function.hash(value, this.prime) % this.size);
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
        return Math.pow(1 - Math.exp(-this.k * (double)this.n / this.size), this.k);
    }

    public static void main(String[] args) {
        int n = 10_000;
        int range = 100_000_000;
        double factor = 10;
        int size = (int) Math.round(factor * n);
        int k = 1; // Number of hash functions

        Random random = new Random(0);
        BloomFilter bf = new BloomFilter(size, k, n);
        HashSet<Integer> set = new HashSet<>(n);
        System.out.println(bf.primeNumber());

        while (set.size() < n) {
            set.add(random.nextInt(range));
        }

        for (int item : set) {
            bf.add(item);
        }

        int TP = 0, FP = 0, TN = 0, FN = 0;

        for (int i = 0; i < range; i++) {
            int key = i; //random.nextInt(range);
            Boolean containsBF = bf.contains(key);
            Boolean containsHS = set.contains(key);

            if (containsBF && containsHS) {
                TP++;
            } else if (!containsBF && !containsHS) {
                TN++;
            } else if (!containsBF && containsHS) {
                FN++;
            } else if (containsBF && !containsHS) {
                FP++;
            }
        }

        System.out.println("TP = " + String.format("%6d", TP) + "\tTPR = "
                + String.format("%1.4f", (double) TP / (double) n));
        System.out.println("TN = " + String.format("%6d", TN) + "\tTNR = "
                + String.format("%1.4f", (double) TN / (double) (range - n)));
        System.out.println("FN = " + String.format("%6d", FN) + "\tFNR = "
                + String.format("%1.4f", (double) FN / (double) (n)));
        System.out.println("FP = " + String.format("%6d", FP) + "\tFPR = "
                + String.format("%1.4f", (double) FP / (double) (range - n)));
        System.out.println("Expected FPR = " + bf.calculateExpectedFP());
    }
}
