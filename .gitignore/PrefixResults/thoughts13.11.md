started reading the paper "Prefix Filter: Practically and Theoretically Better Than
Bloom" https://arxiv.org/pdf/2203.17139

### takeaways for the introduction
- approximate membership query is what the filter should answer
  - only yes or no if element is in data
  - FP happen, no FN <br/>
  -> my Implementation has FN, because I check if a Prefix that once was in the Filter isn't anymore<br/>
  -> maybe change Implementation<br/>
- important Characteristics
  - space
  - query throughput
  - insertion throughput and build time
- Parameters
  - Universe u from which the Filter is build
  - upper bound n for number of keys per set<br/>
  -> maybe no need for in my case<br/>
  -> upper bound for number of Prefixes: (num_characters)^Prefix_size<br/>
  - upper bound epsilon for FP
- this Prefix filter is only indirectly connected to my Prefix Filter
  - does store Fingerprints which are hash values
  - does have two cache lines, one for the bins, one for the spare
  - smart displacement strategies, keep maximal fingerprint