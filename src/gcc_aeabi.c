unsigned int __udiv(unsigned int nom, unsigned int den)
{
    int result = 0;

    if (den == 0) {
        return 0;
    }

    while (nom >= den) {
        nom -= den;
        result++;
    }

    return result;
}


unsigned int __umod(unsigned int num, unsigned int mod)
{
    unsigned int div = __udiv(num, mod);

    if (div == 0) {
        return num;
    }

    return num - (mod * div);
}
