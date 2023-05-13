import pickle

with open('signatures.pkl', 'rb') as f:
    result = pickle.load(f)
    print(result)