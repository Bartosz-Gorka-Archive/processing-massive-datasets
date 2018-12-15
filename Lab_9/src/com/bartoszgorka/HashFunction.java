package com.bartoszgorka;

public class HashFunction {
    private int a;
    private int b;

    public HashFunction(int a, int b) {
        this.a = a;
        this.b = b;
    }

    public int hash(int x, int prime) {
        return (this.a * x + this.b) % prime;
    }
}
