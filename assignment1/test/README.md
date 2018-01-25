# LICENSE

[CC Zero](https://wiki.creativecommons.org/wiki/Public_domain)

The code provided here is meant as a starting point or study
guide for the assignment only. There are other ways of 
solving the assignment of course, with very different designs.

Also, note that re-using any of the code listed here must be done
in accordance with the UofA's Code of Student Conduct.


# What are these "documents"?

Each document in the test case is a statement in a true/false question about stemming. Some of those statements are **false**, BTW.

# Test Cases:

query: Stemming
answer: [doc1, doc2, doc3, doc4]

query: Stemming
answer: [doc1, doc2, doc3, doc4]

query: system AND recall
answer: [doc2]

query: system OR vocabulary
answer: [doc1, doc2, doc3]

query: system AND (recall OR precision)
answer: [doc1, doc2]

query: (recall OR precision) AND system
answer: [doc1, doc2]

query: time OR (precision AND while)
answer: [doc4]

query: (precision AND while) OR time
answer: [doc4]

query: system OR vocabulary OR time
answer: [doc1, doc2, doc3, doc4]

query: system AND never AND precision
answer: [doc1]

query: system OR vocabulary OR while AND at OR should
answer: [doc4]

query: "stemming should" OR "stemming increases"
answer: [doc3, doc4]

query: "stemming never" AND "stemming increases"
answer: []

