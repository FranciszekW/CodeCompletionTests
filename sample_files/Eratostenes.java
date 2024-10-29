public class Eratostenes {

    /**
     * prints out all primes smaller than max
     * @param max upper bound for finding primes
     */
    private static void printPrimes(int max) {
        boolean isPrime[] = new boolean[max];
        for (int i = 2; i < max; ++i) {
            isPrime[i] = true; // numbers bigger than 1 have a potential to be prime
        }
        for (int i = 2; i * i < max; ++i) {
            if (isPrime[i]) {
                for (int k = 0; i * i + k * i < max; ++k) { // we jump by i crossing out all complex numbers
                    isPrime[i * i + i * k] = false;
                }
            }
        }
        for (int i = 0; i < max; ++i) {
            if (isPrime[i]) {
                System.out.print(i);
                System.out.print(' ');
            }
        }
    }

    public static void main(String[] args) {
        int max = Integer.parseInt(args[0]);
        printPrimes(max);
    }
}
