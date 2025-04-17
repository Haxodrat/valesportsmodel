# models.py

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from transformers import AutoTokenizer, AutoModel
import torch

class FeatureEngineer:
    def __init__(self, text_model_name="distilbert-base-uncased"):
        # load a lightweight transformer for text embeddings
        self.tokenizer = AutoTokenizer.from_pretrained(text_model_name)
        self.text_model = AutoModel.from_pretrained(text_model_name)
    
    def embed_text(self, texts: pd.Series) -> pd.DataFrame:
        """
        Take a Series of strings (e.g. news headlines), return a DataFrame
        of fixed‐size embeddings (e.g. mean‐pooled).
        """
        embeddings = []
        for txt in texts.fillna("").tolist():
            inputs = self.tokenizer(txt, return_tensors="pt", 
                                     truncation=True, max_length=64)
            with torch.no_grad():
                outputs = self.text_model(**inputs)
            # mean‐pool the token embeddings
            emb = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            embeddings.append(emb)
        return pd.DataFrame(embeddings, 
                            columns=[f"text_emb_{i}" for i in range(embeddings[0].shape[0])])
    
    def prepare_features(self,
                         team_stats: pd.DataFrame,
                         rankings: pd.DataFrame,
                         player_stats: pd.DataFrame,
                         news: pd.DataFrame) -> pd.DataFrame:
        """
        Join your numeric tables on match_id, merge the text embeddings,
        and return a clean X matrix.
        """
        # 1) merge team_stats, rankings, player_stats on match ID
        df = team_stats.merge(rankings, on="match_id") \
                       .merge(player_stats, on="match_id")
        
        # 2) produce text embeddings from latest news headlines
        text_emb = self.embed_text(news["headline"])
        text_emb["match_id"] = news["match_id"]
        
        # 3) merge text embeddings into df
        df = df.merge(text_emb, on="match_id", how="left").fillna(0)
        
        # drop any non‑feature columns
        return df.drop(columns=["match_id"])

class EsportsPredictor:
    def __init__(self, params=None):
        self.params = params or {
            "objective": "binary",
            "metric": "auc",
            "boosting_type": "gbdt",
            "verbosity": -1
        }
        self.model = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the LightGBM model on your features X and binary label y.
        """
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        train_data = lgb.Dataset(X_train, label=y_train)
        valid_data = lgb.Dataset(X_val, label=y_val)
        self.model = lgb.train(
            self.params,
            train_data,
            valid_sets=[valid_data],
            early_stopping_rounds=50,
            verbose_eval=20
        )
        # quick eval
        preds = self.model.predict(X_val)
        print("Validation AUC:", roc_auc_score(y_val, preds))

    def predict_proba(self, X: pd.DataFrame) -> pd.Series:
        """
        Return the probability that team1 wins.
        """
        return pd.Series(self.model.predict(X), index=X.index)

    def predict(self, X: pd.DataFrame, threshold=0.5) -> pd.Series:
        """
        Return 0/1 predictions based on threshold. 
        """
        return (self.predict_proba(X) >= threshold).astype(int)
