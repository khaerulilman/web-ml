# apriori_logic.py
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def apriori_model(dataset, min_support=0.3, min_confidence=0.6):
    """
    Generate association rules using Apriori algorithm
    
    Args:
        dataset: List of transactions, where each transaction is a list of items
        min_support: Minimum support threshold (default: 0.3)
        min_confidence: Minimum confidence threshold (default: 0.6)
    
    Returns:
        pandas.DataFrame: DataFrame containing association rules
    """
    try:
        # Validasi input
        if not dataset or len(dataset) == 0:
            print("Dataset kosong")
            return pd.DataFrame()
        
        # Validasi bahwa setiap transaksi tidak kosong
        valid_transactions = [trans for trans in dataset if trans and len(trans) > 0]
        if not valid_transactions:
            print("Tidak ada transaksi yang valid")
            return pd.DataFrame()
        
        print(f"Memproses {len(valid_transactions)} transaksi")
        
        # Transaction encoding
        te = TransactionEncoder()
        te_array = te.fit(valid_transactions).transform(valid_transactions)
        df = pd.DataFrame(te_array, columns=te.columns_)
        
        print(f"Data shape: {df.shape}")
        print(f"Kolom: {list(df.columns)}")
        
        # Generate frequent itemsets
        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
        
        if frequent_itemsets.empty:
            print("Tidak ada frequent itemsets yang ditemukan")
            return pd.DataFrame()
        
        print(f"Frequent itemsets: {len(frequent_itemsets)}")
        
        # Generate association rules
        rules = association_rules(
            frequent_itemsets, 
            metric="confidence", 
            min_threshold=min_confidence
        )
        
        if rules.empty:
            print("Tidak ada rules yang ditemukan")
            return pd.DataFrame()
        
        print(f"Rules ditemukan: {len(rules)}")
        
        # Return selected columns
        return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    
    except Exception as e:
        print(f"Error in apriori_model: {str(e)}")
        return pd.DataFrame()