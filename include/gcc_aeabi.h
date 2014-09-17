#ifndef GCC_AEABI_H_
#define GCC_AEABI_H_

/*
 * This header exist since we don't success to use / with gcc.
 * It create bad opcode for cortex-m0. I don't know where is
 * the problem so I will for gcc to not use _thumb function
 * in waiting of a real solution
 */

unsigned int __udiv(unsigned int nom, unsigned int den);
unsigned int __umod(unsigned int num, unsigned int mod);

#endif // GCC_AEABI_H_
