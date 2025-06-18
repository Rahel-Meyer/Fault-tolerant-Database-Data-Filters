# Choice of n

Prefix length n dependent on size of Universe U over which the filter is build. <br/>
If prefix length equals maximal number of prefixes m, the Universe is too large for that n. <br/>

#### Calculation for maximum size of U per n
- **Approximation of Prefix Filter Size:**
  - `max_num_prefixes  m = num_characters^n`
  - `prob_prefix_in_filter = 1 - (1 - 1 / m)^len(data) U`
  - `apprx_num_prefixes p = m * prob_prefix_in_filter`
  - in this case `p=m`
  - `max_U = ln(1-p/m)/ln(1-1/m)`
- Alphabetic Data:
  - n=1, m=52, max_U=`ln((1-52)/52)/ln(1-1/52)`=162
  - n=2, m=2 704, max_U=8 493
  - n=3, m=140 608, max_U=441 731
  - these max_U don`t use the max_num_prefixes, but a number close to it
- Numeric data:
  - n=1, m=10, max_U=29 (should be a bit lower)
  - n=2, m=100, max_U=312
  - n=3, m= 1 000, max_U=3 140
- Printable Data:
  - n=1, m=100, max_U=312
  - n=2, m=10 000, max_U=31 414
  - n=3, m=1 000 000, max_U=3 141 591

## wrong thoughts form 8.11

Prefix length n should be chosen dependent on the number of Entry's N. <br/>
Coupon collector's problem<br/>
k = number of possible Prefixes (all combinations of Symbols) = number Symbols ^ n<br/>
gamma = 0.5772156649 = Euler–Mascheroni constant. <br/>
maximal number of entries per Prefix length approximately = k * ln(k) + gamma * k<br/>
if we use more entry's, we have no true negatives. Filter contains al possible prefixes.<br/>
<br/>
Alphabetic Data:
- n = 1, k = 52, max_num_entry's = 235.46
- n = 2, k = 2704, max_num_entry's = 22 928.53
- n = 3, k = 140608, max_num_entry's = 1 747 860.24
<br/>

Numeric Data:
- n = 1, k = 10, max_num_entry's = 28.79
- n = 2, k = 100, max_num_entry's = 518.21
- n = 3, k = 1 000, max_num_entry's = 7 484.755
<br/>

Printable Data:
- n = 1, k = 100, max_num_entry's = 518.21
- n = 2, k = 1 000, max_num_entry's = 7 484.755
- n = 3, k = 10 000, max_num_entry's = 69 654.55
