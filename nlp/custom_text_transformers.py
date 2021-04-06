import sys
import numpy as np
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

# Defining tokenizer estimator:
class TextTokenizer(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for tokenizing text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        def tokenizer(text):
            '''
            It recieves an array of messages, and for each message: splits text into
            tokens, applies lemmatization, transforms to lowercase, removes blank
            spaces and stop-words.
            Input:
            X: array of text messages
            Output:
            tok_text: message after the transformations
            '''
            # Getting list of all urls using regex:
            detected_urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # Replacing each url in text string with placeholder:
            for url in detected_urls:
                text = text.replace(url, 'urlplaceholder')
            # Extracting tokens from text:
            tokens = word_tokenize(text)
            # Instantiating Lemmatizer object:
            lemmatizer = WordNetLemmatizer()
            # Applying transformations:
            clean_tokens = []
            for tok in tokens:
                # Lemmatizing, trnasforming to lowercase, and removing blank spaces:
                clean_tok = lemmatizer.lemmatize(tok).lower().strip()
                # Adding transformed token to clean_tokens list:
                clean_tokens.append(clean_tok)
            # Removing stopwords:
            stopwords_list = list(set(stopwords.words('english')))
            clean_tokens = [token for token in clean_tokens if token not in stopwords_list]
            # Return from tokenizer function:
            tok_text = ' '.join(clean_tokens)
            return tok_text
        # If activate parameter is set to True:
        if self.activate:
            # Return from transform method:
            return pd.Series(X).apply(tokenizer).values
        # If activate parameter is set to False:
        else:
            pass

# Defining modal verb counter estimator to create new feature:
class ModalVerbCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting modal verbs occurances in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts the number of modal verbs
        for each message.
        Input:
        X: array of text messages
        Output:
        n_md_arr: array with the number of modal verbs for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_md_list = list()
            # Counting modal verbs:
            for text in X:
                n_md = 0
                tokens = word_tokenize(text.lower())
                for tok, pos in nltk.pos_tag(tokens):
                    if pos == 'MD':
                        n_md += 1
                n_md_list.append(n_md)
            # Transforming list into array:
            n_md_arr = np.array(n_md_list)
            n_md_arr = n_md_arr.reshape((len(n_md_arr),1))
            return n_md_arr

        # If activate parameter is set to False:
        else:
            pass

# Defining numeral counter estimator to create new feature:
class NumeralCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting numeral occurances in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts numeral occurances for each
        message.
        Input:
        X: array of text messages
        Output:
        n_cd_arr: array with the number of numeral occurances for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_cd_list = list()
            # Counting numeral occurances:
            for text in X:
                n_cd = 0
                tokens = word_tokenize(text.lower())
                for tok, pos in nltk.pos_tag(tokens):
                    if pos == 'CD':
                        n_cd += 1
                n_cd_list.append(n_cd)
            # Transforming list into array:
            n_cd_arr = np.array(n_cd_list)
            n_cd_arr = n_cd_arr.reshape((len(n_cd_arr), 1))
            return n_cd_arr

        # If activate parameter is set to False:
        else:
            pass

# Defining electricity words counter estimator to create new feature:
class ElectricityWordCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting number of electricity words in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts the number of characters
        for each message.
        Input:
        X: array of text messages
        Output:
        elec_words_arr: array with the number of electricity words for each
        message.
        '''
        # If activate parameter is set to True:
        if self.activate:
            elec_words_count = list()
            elec_list = ['electricity', 'power', 'energy', 'dark']
            # Counting electricity words:
            for text in X:
                # Creating empty list:
                elec_words = 0
                tokens = word_tokenize(text.lower())
                for word in tokens:
                    if word in elec_list:
                        elec_words += 1
                elec_words_count.append(elec_words)
            # Transforming list into array:
            elec_words_arr = np.array(elec_words_count)
            elec_words_arr = elec_words_arr.reshape((len(elec_words_arr), 1))
            return elec_words_arr

        # If activate parameter is set to False:
        else:
            pass

# Defining character counter estimator to create new feature:
class CharacterCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting number of characters in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts the number of characters
        for each message.
        Input:
        X: array of text messages
        Output:
        n_caract: array with the number of characters for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            n_caract = list()
            # Counting characters:
            for text in X:
                n_caract.append(len(text))
            # Transforming list into array:
            n_caract = np.array(n_caract)
            n_caract = n_caract.reshape((len(n_caract),1))
            return n_caract

        # If activate parameter is set to False:
        else:
            pass

# Defining capital letter counter estimator to create new feature:
class CapitalLetterCounter(BaseEstimator, TransformerMixin):
    '''
    Customized transformer for counting capital letters occurances in text.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and counts the number of capital
        letters for each message.
        Input:
        X: array of text messages
        Output:
        cap_count_arr: array with the number of capital letters for each message
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            cap_count_list = list()
            # Verifying each character to see whether it's a capital letter or not:
            for i in range (len(X)):
                cap_count = 0
                msg = X[i]
                for j in range(len(msg)):
                    if msg[j].isupper():
                        cap_count += 1
                cap_count_list.append(cap_count)
            # Transforming list into array:
            cap_count_arr = np.array(cap_count_list)
            cap_count_arr = cap_count_arr.reshape((len(cap_count_arr),1))
            return cap_count_arr

        # If activate parameter is set to False:
        else:
            pass

# Defining first person pronoun estimator to create new feature:
class StartsWithFirstPersonPron(BaseEstimator, TransformerMixin):
    '''
    Customized transformer to check if the message starts with a first person
    pronoun.
    '''
    # Adding 'activate' parameter to activate the transformer or not:
    def __init__(self, activate = True):
        self.activate = activate

    # Defining fit method:
    def fit(self, X, y = None):
        return self

    # Defining transform method:
    def transform(self, X):
        '''
        It recieves an array of messages and evaluates whether each message
        starts with one of the first person pronouns (I, my, we, our).
        Input:
        X: array of text messages
        Output:
        first_person_arr: array indicating whether each message starts with
        first person pronoun
        '''
        # If activate parameter is set to True:
        if self.activate:
            # Creating empty list:
            first_person = list()
            # Creating list to target first person pronouns:
            pron_list = ['i', 'my', 'we', 'our']
            # Tokenizing message and verifying whether first token is a first
            # person pronoun in the list or not:
            for text in X:
                tokens = word_tokenize(text.lower())
                if len(tokens) > 0:
                    if tokens[0] in pron_list:
                        first_person.append(1)
                    else:
                        first_person.append(0)
                else:
                    first_person.append(0)
            # Transforming list into array:
            first_person_arr = np.array(first_person)
            first_person_arr = first_person_arr.reshape((len(first_person_arr),1))
            return first_person_arr

        # If activate parameter is set to False:
        else:
            pass
