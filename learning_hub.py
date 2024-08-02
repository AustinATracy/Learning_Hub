import learning_base as lb

class my_learing_exercises():
    def __init__(self,my_learning_df_instance,location):
        self.my_learning_df = my_learning_df_instance
        self.location = location # the file location to save this to
    def select_a_question(self):
        """Gets an index for a question."""
        return self.my_learning_df.df.apply(lambda row: row["Streak"] * row["Priority"], axis=1).sort_values().index[0]
    def framework_for_learning(self,the_grader):
        """One can plug in a grader and go off"""
        while True:
            id_of_question = self.select_a_question()
            question_information = self.my_learning_df.df.loc[id_of_question]
            user_answer = input(question_information["Question"] + "\n")
            if user_answer == "QQQ":
                break
            if the_grader(user_answer,question_information):
                self.my_learning_df.correct_answer_update(id_of_question)
            else:
                self.my_learning_df.incorrect_answer_display(id_of_question)
                self.my_learning_df.incorrect_answer_update(id_of_question)
            self.my_learning_df.df.to_pickle(self.location)
            self.my_learning_df.df.to_csv(self.location.replace(".pkl",".csv"))
    def exact_match_learn(self):
        def exact_match(user_answer,question_information):
            if user_answer in question_information["Correct Associations"]:
                return True
            else:
                return False
        self.framework_for_learning(exact_match)
    def association_learn(self):
        def association_learn(user_answer,question_information):
            testing_details = True
            search_index = lb.SentenceIndex()
            # Add some sample sentences
            search_index.add_sentences(question_information["Correct Associations"] + 
                                       question_information["Incorrect Associations"])
            
            # Find closest sentences to a query
            closest_sentences = search_index.find_closest(user_answer)
            valid_association_test = [sentence[0] in question_information["Correct Associations"] for sentence in closest_sentences]
            valid = True # assumed true
            if True in valid_association_test:
                if False in valid_association_test:
                    last_index_of_true = len(valid_association_test) - 1 - valid_association_test[::-1].index(True)
                    first_index_of_false = valid_association_test.index(False)
                    if first_index_of_false < last_index_of_true:
                        valid = False
            else:
                valid = False
            valid

            if testing_details:
                print(f"Determination: {valid}")
                print(f"Validity pattern: {valid_association_test}")
                print(f"Sentences behind validity pattern: {closest_sentences}")
            return valid
        self.framework_for_learning(association_learn)

