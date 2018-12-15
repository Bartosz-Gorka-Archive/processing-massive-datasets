package com.bartoszgorka;

public class HashFunction {
    private long a;
    private long b;

    public HashFunction(long a, long b) {
        this.a = a;
        this.b = b;
    }

    public long hash(int x, long prime) {
        return (this.a * (long)x + this.b) % prime;
    }
}
