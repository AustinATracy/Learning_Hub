from importlib import reload # Python 3.4+
import learning_base as lb
import learning_hub as lh
df = lb.my_learing_df()
df.load_learning_df("test.pkl")
learning_exercises = lh.my_learing_exercises(df,"test.pkl")
learning_exercises.association_learn()

