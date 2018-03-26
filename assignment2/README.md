# Assignment 2 README:

## compilation and execution instructions
Require nltk library. To install nltk, run:  
`sudo pip3 install -U nltk`

### create_lms
1. create_lms will create a language model for each document in the corpus.  
2. The language model will save as **"LMS.txt"** in the **[output_dir]**.  
3. create_lms will only read file that has format: **doc_##_??.txt**  

Usage: `$python3 create_lms.py [document_dir] [output_dir]`

### print_lms
1. **[language_models_location]** is the directory that contain the language model file: "LMS.txt".  

Usage: `python3 print_lms.py [language_models_location]`

### query_lms
1. The query should input as a single argument  

Usage: `$python3 query_lms.py [language_models_location] [whitespace-separated multi-term query]`

### nb_classifier
1. The index file for the train set should in the **[train_set_dir]** named as **"index"**
2. The index file for the test set should in the **[test_set_dir]** named as **"index"**

Usage: `$python3 nb_classifier.py [train_set_dir] [test_set_dir]`

## Library
Used "nltk library", "wordpunct_tokenize" package.  
It is a regular-expression based tokenizer that provide efficient tokenization function
and does not require other pre-installed module.
Used 'nltk.corpus.stopwords' to remove stopwords from vocabulary V in training Naive Bayes classifier

## collaborations and websites/resources
Progress Bar Code Reference:  
Code reference: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3

## test cases
test cases and its running instructions are in the `test` folder
