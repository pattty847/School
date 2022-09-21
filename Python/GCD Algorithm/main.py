class GCD:
    """Simple algorithm to calculate greatest common divisor of m and n"""
    def get_gcd_1(self, m, n):
        if m == 0:
            return n
        return self.get_gcd_1(m=n%m, n=m)


    def get_gcd_2(self, m, n):
        while n:
            m, n = n, m % n
        return m
    
gcd = GCD()
print(gcd.get_gcd_1(119, 544))
print(gcd.get_gcd_2(119, 544))