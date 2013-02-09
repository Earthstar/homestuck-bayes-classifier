# Naive Bayes implementation
# For each character, strip quirks?
# Find total frequencies of words
# Find frequency of the appearance of each word in training set for each class
# Calculate conditional probabilities of finding each word for each character
# Assume uniform priors

import collections
import string
import re
import math

class Model:
    def __init__(self, file_list, dict_files = None):
        '''
        self.total_dict - dict of word:frequency for all files
        self.class_dict - dict of classname:word frequency dict
        self.total_wordcounts - dict of classname:total num words in training set
        self.bayes_dict - dict of classname: bayesdict
        '''
        # for each file in the file list, treat it as a class
        # dict_files are previously-made dictionaries stored as .txt
        self.total_dict = collections.defaultdict(int)
        self.class_dict = {}
        if dict_files != None:
            pass
        else:
            for f in file_list:
                name = re.split('[_.]', f)[0]
                self.class_dict[name] = self.make_class_dictionary(f)
                self.merge_dictionary(self.class_dict[name])
        
        self.total_wordcounts = self.count_words()
        for class_name in self.class_dict.keys():
            self.total_wordcounts[class_name] = self.find_total_wordcount(self.class_dict[class_name])
        self.bayes_dict = {}
        # store number of words in class training data
        self.training_word = {}
        for class_name in self.class_dict.keys():
            self.bayes_dict[class_name] = self.bayes_model(class_name)
    
    def make_class_dictionary(self, file_name):
        '''
        for file_name, returns a default dictionary of word:frequency
        '''
        freq_dict = collections.defaultdict(int)
        f = open(file_name, 'r')
        # for each line, strip punctuation, and turn into list of words
        for line in f:
            stripped = string.translate(line, None, string.punctuation)
            stripped = stripped.lower()
            line_list = stripped.split()
            for word in line_list:
                freq_dict[word] += 1
        return freq_dict

    def merge_dictionary(self, d):
        '''
        Merges dictionary with self.total_dict
        '''
        for key in d.keys():
            self.total_dict[key] += d[key]

    def find_total_wordcount(self, d):
        total = 0
        for key in d.keys():
            total += d[key]
        return total

    def count_words(self):
        '''
        returns dictionary of class:total num words
        '''
        d = {}
        for class_name in self.class_dict.keys():
            num_words = 0
            for key in self.class_dict[class_name].keys():
                num_words += self.class_dict[class_name][key]
            d[class_name] = num_words
        return d

    def bayes_model(self, doc_class):
        '''
        Given the name of a document class, creates a Naive Bayesian frequency
        model of all the words. Dictionary stores logs to make calculation
        easier
        '''
        bayes_dict = {}
        num_words = self.total_wordcounts[doc_class]
        for word in self.class_dict[doc_class].keys():
            bayes_dict[word] = math.log(float(self.class_dict[doc_class][word] + 1)/(num_words + len(self.total_dict.keys())))
        return bayes_dict

    def print_frequencies(self, doc_class):
        '''
        Prints words found in doc_class in order of frequency
        '''
        sorted_words = sorted(self.class_dict[doc_class],
                              key = lambda key:self.class_dict[doc_class][key],
                              reverse = True)
        for word in sorted_words:
            print word, self.class_dict[doc_class][word]

    def predict_class(self, file_name):
        '''
        file_name = .txt file of unknown class
        Output = a list of classes in order of likelihood.
        '''
        # take file and turn it into a dictionary of words
        file_dict = collections.defaultdict(int)
        f = open(file_name, 'r')
        for line in f:
            stripped = string.translate(line, None, string.punctuation)
            stripped = stripped.lower()
            line_list = stripped.split()
            for word in line_list:
                file_dict[word] += 1
        # Calculate the probability of document being in each class
        class_prob = {}
        for doc_class in self.class_dict.keys():
            prob = 0
            for word in file_dict.keys():
                if word in self.class_dict[doc_class]:
                    prob += self.class_dict[doc_class][word]*file_dict[word]
                else:
                    # if word not previously encountered, then prob is
                    # total num words in class + num unique words
                    prob += 1.0/(len(self.class_dict[doc_class].keys()) + len(self.total_dict.keys()))
            class_prob[doc_class] = prob
        return class_prob
