# Python3 program Miller-Rabin randomized primality test
# Copied from geeksforgeeks: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
import random 

# Utility function to do 
# modular exponentiation. 
# It returns (x^y) % p 
def power(x, y, p): 
	
	# Initialize result 
	res = 1; 
	
	# Update x if it is more than or 
	# equal to p 
	x = x % p; 
	while (y > 0): 
		
		# If y is odd, multiply 
		# x with result 
		if (y & 1): 
			res = (res * x) % p; 

		# y must be even now 
		y = y>>1; # y = y/2 
		x = (x * x) % p; 
	
	return res; 

# This function is called 
# for all k trials. It returns 
# false if n is composite and 
# returns false if n is 
# probably prime. d is an odd 
# number such that d*2<sup>r</sup> = n-1 
# for some r >= 1 
def miillerTest(d, n): 
	
	# Pick a random number in [2..n-2] 
	# Corner cases make sure that n > 4 
	a = 2 + random.randint(1, n - 4); 

	# Compute a^d % n 
	x = power(a, d, n); 

	if (x == 1 or x == n - 1): 
		return True; 

	# Keep squaring x while one 
	# of the following doesn't 
	# happen 
	# (i) d does not reach n-1 
	# (ii) (x^2) % n is not 1 
	# (iii) (x^2) % n is not n-1 
	while (d != n - 1): 
		x = (x * x) % n; 
		d *= 2; 

		if (x == 1): 
			return False; 
		if (x == n - 1): 
			return True; 

	# Return composite 
	return False; 

# It returns false if n is 
# composite and returns true if n 
# is probably prime. k is an 
# input parameter that determines 
# accuracy level. Higher value of 
# k indicates more accuracy. 
def isPrime( n, k): 
	
	# Corner cases 
	if (n <= 1 or n == 4): 
		return False; 
	if (n <= 3): 
		return True; 

	# Find r such that n = 
	# 2^d * r + 1 for some r >= 1 
	d = n - 1; 
	while (d % 2 == 0): 
		d //= 2; 

	# Iterate given nber of 'k' times 
	for i in range(k): 
		if (miillerTest(d, n) == False): 
			return False; 

	return True; 

# Driver Code 
# Number of iterations 
k = 4; 

print("All primes smaller than 100: "); 
for n in range(1,100): 
	if (isPrime(n, k)): 
		print(n , end=" "); 

# This code is contributed by mits (see citation above)

# Get a random triple (p, a, b) where p is prime and a,b are numbers betweeen 2 and p-1
def get_random_hash_function():
    n = random.getrandbits(64)
    if n < 0: 
        n = -n 
    if n % 2 == 0:
        n = n + 1
    while not isPrime(n, 20):
        n = n + 1
    a = random.randint(2, n-1)
    b = random.randint(2, n-1)
    return (n, a, b)

# hash function fora number
def hashfun(hfun_rep, num):
    (p, a, b) = hfun_rep
    return (a * num + b) % p

# hash function for a string.
def hash_string(hfun_rep, hstr):
    n = hash(hstr)
    return hashfun(hfun_rep, n)    

# Let us load the "Great Gatsby" novel and extract all words of length 5 or more
filename = './great-gatsby-fitzgerald.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_gg = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_gg))
# Let us count the precise word frequencies
word_freq_gg = {}
for elt in longer_words_gg:
    if elt in word_freq_gg:
        word_freq_gg[elt] += 1
    else:
        word_freq_gg[elt] = 1
print(len(word_freq_gg))

# Let us load the "War and Peace" novel by Tolstoy translation and extract all words of length 5 or more
filename = './war-and-peace-tolstoy.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_wp = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_wp))
word_freq_wp = {}
for elt in longer_words_wp:
    if elt in word_freq_wp:
        word_freq_wp[elt] += 1
    else:
        word_freq_wp[elt] = 1
print(len(word_freq_wp))

class CountMinSketch:
    # Initialize with `num_counters`
	def __init__ (self, num_counters):
		self.m = num_counters
		self.hash_fun_rep = get_random_hash_function()
		self.counters = [0]*self.m
    
    
    # function: increment 
    # given a word, increment its count in the countmin sketch
	def increment(self, word):
		# your code here
		idx = hash_string(self.hash_fun_rep, word)
		self.counters[idx%self.m] += 1
		
    # function: approximateCount
    # Given a word, get its approximate count
	def approximateCount(self, word):
		# your code here
		idx = hash_string(self.hash_fun_rep, word)
		min_count = self.counters[idx%self.m]
		return min_count

def initialize_k_counters(k, m): 
    return [CountMinSketch(m) for i in range(k)]

# Function increment_counters
# increment each of the individual counters with the word
def increment_counters(count_min_sketches, word):
    # your code here
    for cms in count_min_sketches:
        cms.increment(word)
        
# Function: approximate_count
# Get the approximate count by querying each counter bank and taking the minimum
def approximate_count(count_min_sketches, word):
	return min([cms.approximateCount(word) for cms in count_min_sketches])

cms_list = initialize_k_counters(5, 1000)
for word in longer_words_gg:
    increment_counters(cms_list, word)

discrepencies = []
for word in longer_words_gg:
    l = approximate_count(cms_list, word)
    r = word_freq_gg[word]
    assert ( l >= r)
    discrepencies.append( l-r )

assert(max(discrepencies) <= 200), 'The largest discrepency must be definitely less than 200 with high probability. Please check your implementation'
print('Passed all tests: 10 points')