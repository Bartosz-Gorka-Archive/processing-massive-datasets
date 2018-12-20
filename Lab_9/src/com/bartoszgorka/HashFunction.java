package com.bartoszgorka;

/**
 * Hash Function class
 * Each function as expression: (ax + b) % prime
 */
public class HashFunction {
    private long a;
    private long b;

    /**
     * Hash Function constructor
     * @param a Parameter a
     * @param b Parameter b
     */
    public HashFunction(long a, long b) {
        this.a = a;
        this.b = b;
    }

    /**
     * Generate hash value
     * @param x Value from user
     * @param prime Prime number - modulo operation base
     * @return Hashed value
     */
    public long hash(long x, long prime) {
        return (this.a * x + this.b) % prime;
    }
}
