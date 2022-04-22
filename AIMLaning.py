

class BayesCat(object):
    """
    generates an object that classifies provided data based on a set of training data
    """

    def __init__(self, category_data, train_data, benign_words='', delimiter=' '):
        """
        input parameter:    cat_data
        data type:          array
        description:        ordered list of the category field. This list of categories
                            corresponds to the train_data input.

        input parameter:    train_data
        data type:          array
        description:        ordered list of the text that is being parsed and used to determine
                            what text is associated with the categories.

        input parameter:    benign_words
        data type:          array
        description:        Set of words that can be ignored.
        """

        self._cat_scores = {}
        self._cat_counts = {}
        self._total_entries = 0
        self._delimiter = delimiter
        if benign_words == '':
            self._benign_words = set()
        else:
            self._benign_words = benign_words
        self.__makeBayes__(category_data, train_data)

    def __makeBayes__(self, category_data, train_data):
        """
        generates the scoring and count dictionaries
        """
        for index, cat in enumerate(category_data):
            if cat not in self._cat_scores:
                self._cat_scores[cat] = {}
                self._cat_counts[cat] = 1
            else:
                self._cat_counts[cat] += 1
            self._total_entries += 1
            parsed_strings = train_data[index].split(self._delimiter)
            self.__cleanStrings__(parsed_strings)
            self.__addToCat__(cat, parsed_strings)

    def __cleanStrings__(self, strings):
        """
        remove any benign words from the list of strings
        """
        for word in strings:
            if word in self._benign_words:
                strings.remove(word)

    def __addToCat__(self, category, strings):
        """
        adds all sequential combinations of the provided list of strings to the provided category
        in the cat_scores dictionary
        """

        for index1 in range(len(strings)):
            for index2 in range(index1, len(strings)):
                this_addition = ''
                for this_idx in range(index1, index2+1):
                    this_addition += ' '
                    this_addition += strings[this_idx]
                this_addition = this_addition[1:]
                if this_addition not in self._cat_scores[category]:
                    self._cat_scores[category][this_addition] = 1
                else:
                    self._cat_scores[category][this_addition] += 1

    def guess(self, description):
        """
        uses the provided description and returns the category that best matches
        """

        desc_arr = description.split(self._delimiter)
        self.__cleanStrings__(desc_arr)

        top_score = 0
        top_cat = ''

        for cat in self._cat_counts:
            this_score = 0
            for index1 in range(len(desc_arr)):
                for index2 in range(index1, len(desc_arr)):
                    this_str = ''
                    for this_idx in range(index1, index2+1):
                        this_str += ' '
                        this_str += desc_arr[this_idx]
                    this_str = this_str[1:]
                    if this_str in self._cat_scores[cat]:
                        score_add = self._cat_scores[cat][this_str] / self._cat_counts[cat]
                        score_add = score_add * (2 ** (this_str.count(' ')))
                        this_score += score_add
            # this_score *= self._cat_counts[cat] / self._total_entries
            print(cat, this_score)
            if this_score > top_score:
                top_cat = cat
                top_score = this_score
        return top_cat


if __name__ == "__main__":

    fruits = ['apple',
              'apple',
              'apple',
              'apple',
              'orange',
              'orange',
              'banana',
              'banana',
              'pear']
    abouts = ['this fruit is red',
              'this fruit is yellow',
              'this fruit is yellow',
              'this fruit is green',
              'this fruit is orange',
              'this fruit is orange',
              'this fruit is yellow',
              'this fruit is yellow',
              'this fruit is green']

    ignore_words = [
        'this', 'the', 'is'
    ]

    fruit_predictor = BayesCat(fruits, abouts, benign_words=ignore_words)
    print(fruit_predictor.guess('i have myself a green fruit'))
