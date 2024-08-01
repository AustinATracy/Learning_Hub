import pyautogui
import pandas as pd
import time

class my_learing_df():
    def __init__(self):
        self.df = pd.DataFrame(columns=["Question","Correct Associations","Incorrect Associations","Last Correct Answer Date","Streak","Priority","Overall Score","Other Question Padding"])
    def add_row(self,question,correct_associations=[],incorrect_associations=[],last_correct_answer_date=[],streak=0,priority=10,overall_score=0,other_question_padding=0):
        self.df = pd.concat([self.df,pd.DataFrame([{"Question": question, "Correct Associations": correct_associations, "Incorrect Associations": incorrect_associations, "Last Correct Answer Date": last_correct_answer_date, "Streak": streak, "Priority": priority,"Overall Score": overall_score, "Other Question Padding": other_question_padding}],index=[len(self.df)])])
    def correct_answer_update(self,index_of_update):
        self.df.at[index_of_update,"Last Correct Answer Date"] = time.strftime('%m/%d/%y')
        if self.df.at[index_of_update,"Streak"] > -1:
            self.df.at[index_of_update,"Streak"] = self.df.loc[index_of_update,"Streak"] + 1
            # self.df.loc[id_of_question]["Streak"] += 1
        else:
            self.df.at[index_of_update,"Streak"] = 1
        self.df.at[index_of_update,"Overall Score"] = self.df.at[index_of_update,"Overall Score"] + self.df.at[index_of_update,"Streak"]
        self.df["Other Question Padding"] = self.df["Other Question Padding"] + 1 
        self.df.at[index_of_update,"Other Question Padding"] = 0 
    def incorrect_answer_update(self,index_of_update):
        if self.df.at[index_of_update,"Streak"] < 1:
            self.df.at[index_of_update,"Streak"] = self.df.loc[index_of_update,"Streak"] - 1
        else:
            self.df.at[index_of_update,"Streak"] = -1
        self.df.at[index_of_update,"Overall Score"] = self.df.at[index_of_update,"Overall Score"] + self.df.at[index_of_update,"Streak"]
        self.df["Other Question Padding"] = self.df["Other Question Padding"] + 1 
        self.df.at[index_of_update,"Other Question Padding"] = 0
    def incorrect_answer_display(self,index_of_update):
        print("Opps, the correct answer is \n")
        print(self.df.at[index_of_update,"Correct Associations"])
    def save_learning_df(self,location):
        self.df.to_pickle(location)
    def load_learning_df(self,location):
        self.df = pd.read_pickle(location)

class my_learing_exercises_strict():
    def __init__(self,my_learning_df_instance,location):
        self.my_learning_df = my_learning_df_instance
        self.location = location # the file location to save this to
    def select_a_question(self):
        """Gets an index for a question."""
        return self.my_learning_df.df.apply(lambda row: row["Streak"] * row["Priority"], axis=1).sort_values().index[0]
    def learn(self):
        while True:
            id_of_question = self.select_a_question()
            question_information = self.my_learning_df.df.loc[id_of_question]
            user_answer = input(question_information["Question"] + "\n")
            if user_answer == "QQQ":
                break
            if user_answer in question_information["Correct Associations"]:
                self.my_learning_df.correct_answer_update(id_of_question)
            else:
                self.my_learning_df.incorrect_answer_display(id_of_question)
                self.my_learning_df.incorrect_answer_update(id_of_question)
            self.my_learning_df.df.to_pickle(self.location)
            self.my_learning_df.df.to_csv(self.location.replace(".pkl",".csv"))

df = my_learing_df()
df.load_learning_df("test.pkl")

df.add_row("How do you represent the set difference of A and B?",[r"A\B"])

df.add_row("How do you represent the symmetric difference of A and B?",[r"(A\B) U (B\A)"])

df.add_row("How do you represent the symmetric difference of A and B with a symbol?",[r"Plus sign in a circle"])


learning_exercises = my_learing_exercises_strict(df,"test.pkl")

learning_exercises.learn()

# learning_exercises.my_learning_df.df["Streak"] = 0