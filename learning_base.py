from sentence_transformers import SentenceTransformer
import faiss

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

class SentenceIndex:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.sentences = []

    def add_sentences(self, new_sentences):
        self.sentences.extend(new_sentences)
        embeddings = self.model.encode(new_sentences)
        
        if self.index is None:
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
        
        self.index.add(embeddings.astype('float32'))

    def find_closest(self, query, k=5):
        query_embedding = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            results.append((self.sentences[idx], distance))
        
        return results


