exp1 = """

/* factorial.p 
-- 2023-03-20 
-- by jcr 
*/ 

int i; 

// Function that calculates the factorial of a number n 
function fact(n){ 
int res = 1; 
while res > 1 { 
res = res * n; 
res = res - 1; 
} 
} 

// Main program 
program myFact{ 
for i in [1..10]{ 
print(i, fact(i)); 
} 
}


"""

exp2 = """

/* max.p: calculate the largest integer of an unordered list 
-- 2023-03-20 
-- by jcr 
*/ 

int i = 10, a[10] = {1,2,3,4,5,6,7 ,8,9,10}; 

// Main program 
program myMax{ 
int max = a[0]; 
for i in [1..9]{ 
if max < a[i] { 
max = a[i]; 
} 
} 
print(max); 
}

"""