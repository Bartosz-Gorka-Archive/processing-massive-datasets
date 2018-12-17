package com.bartoszgorka;

public class HashFunction {
    private long a;
    private long b;

    public HashFunction(long a, long b) {
        this.a = a;
        this.b = b;
    }

    public long hash(long x, long prime) {
        return (this.a * x + this.b) % prime;
    }
}
