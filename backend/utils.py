from collections import defaultdict
import pandas as pd

def extract_features(data):
    wallet_features = defaultdict(lambda: {
        'total_transactions': 0,
        'num_deposit': 0,
        'num_borrow': 0,
        'num_repay': 0,
        'num_redeem': 0,
        'num_liquidation': 0,
        'total_usd_deposit': 0.0,
        'total_usd_borrow': 0.0,
        'total_usd_repay': 0.0,
        'timestamps': []
    })

    action_map = {
        'deposit': ('num_deposit', 'total_usd_deposit'),
        'borrow': ('num_borrow', 'total_usd_borrow'),
        'repay': ('num_repay', 'total_usd_repay'),
        'redeemunderlying': ('num_redeem', None),
        'liquidationcall': ('num_liquidation', None)
    }

    for tx in data:
        wallet = tx['userWallet']
        action = tx.get('action', '').lower()
        timestamp = tx.get('timestamp')
        wallet_features[wallet]['total_transactions'] += 1

        if timestamp:
            wallet_features[wallet]['timestamps'].append(timestamp)

        if action in action_map:
            count_key, value_key = action_map[action]
            wallet_features[wallet][count_key] += 1

            if value_key and 'amount' in tx['actionData'] and 'assetPriceUSD' in tx['actionData']:
                try:
                    amount = float(tx['actionData']['amount'])
                    price = float(tx['actionData']['assetPriceUSD'])
                    usd_value = (amount / 1e18) * price
                    wallet_features[wallet][value_key] += usd_value
                except:
                    pass

    processed_data = []
    for wallet, features in wallet_features.items():
        timestamps = sorted(features.pop('timestamps'))
        avg_interval = 0
        if len(timestamps) > 1:
            intervals = [t2 - t1 for t1, t2 in zip(timestamps[:-1], timestamps[1:])]
            avg_interval = sum(intervals) / len(intervals)

        repay_borrow_ratio = (
            features['total_usd_repay'] / features['total_usd_borrow']
            if features['total_usd_borrow'] > 0 else 0
        )

        features['wallet'] = wallet
        features['avg_tx_interval'] = avg_interval
        features['repay_borrow_ratio'] = repay_borrow_ratio
        processed_data.append(features)

    return pd.DataFrame(processed_data)
