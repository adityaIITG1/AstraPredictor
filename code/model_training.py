
import pandas as pd, os, joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
BASE=os.path.dirname(os.path.dirname(__file__))
df=pd.read_csv(os.path.join(BASE,'data','supply_log_sample.csv'))
X=df[['Troop_Count','Terrain','Weather']]
y=df[['Fuel_Used','Food_Used','Meds_Used','SpareParts']]
ct=ColumnTransformer([('num','passthrough',['Troop_Count']),
                      ('cat',OneHotEncoder(handle_unknown='ignore'),['Terrain','Weather'])])
model=Pipeline([('prep',ct),
                ('rf',MultiOutputRegressor(RandomForestRegressor(n_estimators=300,random_state=1)))])
model.fit(X,y)
joblib.dump(model, os.path.join(BASE,'code','model.joblib'))
print('Model saved.')
