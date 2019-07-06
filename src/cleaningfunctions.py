import pandas as pd


mean_of_driver = 4.60
mean_by_driver = 4.78

def pipeline_clean(df):
    df['last_trip_date'] = pd.to_datetime(df['last_trip_date'])
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['phone'] = df['phone'].fillna("No phone")
    df['avg_rating_by_driver'].fillna(mean_by_driver, inplace=True)
    df['avg_rating_of_driver'].fillna(mean_of_driver, inplace=True)
    td = df['signup_date'].max() -  df['signup_date']
    df['days_since_signup']=(td.dt.days)
    df.drop(['signup_date'],axis=1,inplace=True)
    df['churned'] = (df['last_trip_date'] < '2014-06-01')
    df.drop(['last_trip_date'],axis=1,inplace=True)
    df = pd.concat([df,pd.get_dummies(df['phone'])],axis=1)
    df.drop(['phone'],axis=1,inplace=True)
    df = pd.concat([df,pd.get_dummies(df['city'])],axis=1)
    df.drop(['city'],axis=1,inplace=True)
    return df


from sklearn.model_selection import train_test_split
def split_data(df):
    X_train, X_cv, y_train, y_cv = train_test_split(df.drop(['churned'],axis=1), df['churned'], test_size=0.2, random_state=42)
    return X_train, X_cv, y_train, y_cv

def rbd(x):
    if x == 5:
        return 5
    elif x >= 4.5:
        return 4.5
    elif x >= 4:
        return 4
    else:
        return 0

def bin_rating_by_driver(df):
    return df.avg_rating_by_driver.apply(lambda x: rbd(x))

def pipeline_clean2(df):
    """Take our dataset and derive days since sign up, fill in NaNs, create our target 
    column and use 'get_dummies' on our categorical vaiables
    ----------------------
    INPUT
    df = Pandas dataframe
    ----------------------
    OUTPUT
    df = Pandas dataframe
    ----------------------
    """
    df['last_trip_date'] = pd.to_datetime(df['last_trip_date'])
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['phone'] = df['phone'].fillna("No phone")
    df['avg_rating_by_driver'].fillna(mean_by_driver, inplace=True)
    df['avg_rating_of_driver'].fillna(mean_of_driver, inplace=True)
    td = df['signup_date'].max() -  df['signup_date']
    df['days_since_signup']=(td.dt.days)
    df.drop(['signup_date'],axis=1,inplace=True)
    df['churned'] = (df['last_trip_date'] < '2014-06-01')
    df.drop(['last_trip_date'],axis=1,inplace=True)
    df = pd.concat([df,pd.get_dummies(df['phone'])],axis=1)
    df.drop(['phone'],axis=1,inplace=True)
    df = pd.concat([df,pd.get_dummies(df['city'])],axis=1)
    df.drop(['city'],axis=1,inplace=True)
    df.avg_rating_by_driver = df.avg_rating_by_driver.apply(lambda x: rbd(x))
    return df
