from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

labels = ['A', 'B', 'C', 'D', 'E']


def create_transactions(df):
    transactions = []
    for index, row in df.iterrows():
        # Using labels list to map indices to labels
        transaction = [labels[i] for i in range(len(row)) if row[i] == 1]
        transactions.append(transaction)
    return transactions


def show_rules(transactions, min_support = 0.3, min_confidence = 0.3):
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

    print("Frequent Itemsets:\n", frequent_itemsets)

    if frequent_itemsets.empty:
        raise ValueError()

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    for _, row in frequent_itemsets.iterrows():
        relevant_rules = rules[rules['antecedents'] == row['itemsets']]
        # print(relevant_rules.empty)
        if not relevant_rules.empty:
            print(f"Items: {', '.join(row['itemsets'])}")
            print(f"Support: {row['support']}")
            print("Rules:")
            # Filter rules that involve the current itemset
            for _, rule_row in relevant_rules.iterrows():
                base_items = ', '.join(rule_row['antecedents'])
                add_items = ', '.join(rule_row['consequents'])
                print(f"    Rule: If a person buys [{base_items}], they will also buy [{add_items}]")
                print(f"    Confidence: {rule_row['confidence']:.2f}")
                print(f"    Lift: {rule_row['lift']:.2f}")
            print("\n")

    return frequent_itemsets, rules