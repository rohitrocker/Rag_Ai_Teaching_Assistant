
    break

# print(my_dicts)

df = pd.DataFrame.from_records(my_dicts)
joblib.dump(df,embeddings.joblib)