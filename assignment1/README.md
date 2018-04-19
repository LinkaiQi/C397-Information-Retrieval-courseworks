# Assignment 1 README:

## compilation and execution instructions
Require nltk library. To install nltk, run:  
`sudo pip3 install -U nltk`

### create_index
create_index.py will create the index file in the current execution path  
`$python3 create_index.py [dir]`

### print_index
`$python3 print_index.py [directory]`

### boolean_query
query should input as a single argument  
`$python3 boolean_query.py [directory] [query]`

### vs_query
`$python3 vs_query.py [index_location] [k] [score] [term1] [term2] [term3] ...`

### create_zone_index
`$python3 create_zone_index.py [doc_dir] [index_dir] ...`

### zone_scorer (This question's solution was submitted after the assignment1 due date)
query `q` should input as a single argument  
`g` is the score weight for 'title' zone, (1 - g) is score weight for 'body' zone  
`$python3 zone_scorer.py [index dir] [k] [g] [q]`

### Tokenization
Using "nltk library", "wordpunct_tokenize" package.  
It is a regular-expression based tokenizer that provide efficient tokenization function
and does not require other pre-installed module.

## collaborations and websites/resources
Boolean query parser (Parsing simple string and generating lisp)  
Code reference: http://kitchingroup.cheme.cmu.edu/blog/2014/03/31/Using-pyparsing-for-search-queries-with-tags/

Progress Bar Code Reference:  
Code reference: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3

## test cases for bonus marks
test cases and its running instructions are in the `test` folder
