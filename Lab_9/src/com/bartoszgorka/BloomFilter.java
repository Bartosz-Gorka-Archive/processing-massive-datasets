package com.bartoszgorka;

import java.math.BigInteger;
import java.util.BitSet;
import java.util.HashSet;
import java.util.Random;

// TODO generator hash functions - generate A, B parameters
// TODO implement add
// TODO implement contains
// TODO calculate stats and verify results

public class BloomFilter {
    int size = 0;
    int n = 0;
    int k = 0;
    BitSet vector;

    private double calculateExpectedFP() {
        return Math.pow(1 - Math.exp(-this.k * (double)this.n / this.size), this.k);
    }

    private BloomFilter(int size, int k, int n) {
        this.size = size;
        this.k = k;
        this.n = n;

        // Set bitset
        this.vector = new BitSet(size);

        // Run generator hash functions
        // TODO
    }


    private BigInteger primeNumber() {
        BigInteger value = new BigInteger(String.valueOf(this.size));
        return value.nextProbablePrime();
    }

    public void add(int key) {
        // TODO
    }

    public Boolean contains(int key) {
        // TODO
        return true;
    }

    public static void main(String[] args) {
        int n = 10_000;
        int range = 100_000_000;
        double factor = 10;
        // M - size bloom filter
        // create x times A i B
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
