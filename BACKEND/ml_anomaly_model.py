import math


def safe_float(value, default=0.0):
    try:
        return float(str(value).replace(',', '').strip() or default)
    except Exception:
        return default


def safe_int(value, default=0):
    try:
        return int(float(str(value).strip() or default))
    except Exception:
        return default


def transaction_features(row):
    amount = safe_float(row.get('TransactionAmount', 0))
    description = str(row.get('TransactionType', '')).strip().lower()
    location = str(row.get('Location', '')).strip().lower()
    login_attempts = safe_int(row.get('LoginAttempts', 0))
    account_balance = safe_float(row.get('AccountBalance', 0))
    transaction_duration = safe_float(row.get('TransactionDuration', 0))
    channel = str(row.get('Channel', '')).strip().lower()

    return {
        'absolute_amount': abs(amount),
        'login_attempts': login_attempts,
        'account_balance': account_balance,
        'transaction_duration': transaction_duration,
        'risk_sensitive_type': 1 if description in ['transfer', 'withdrawal'] else 0,
        'unknown_location': 1 if location == '' or 'unknown' in location else 0,
        'suspicious_channel': 1 if channel in ['unknown', 'other'] else 0,
    }


def train_anomaly_model(rows):
    feature_names = [
        'absolute_amount',
        'login_attempts',
        'account_balance',
        'transaction_duration',
        'risk_sensitive_type',
        'unknown_location',
        'suspicious_channel',
    ]
    vectors = [transaction_features(row) for row in rows]
    stats = {}

    for feature in feature_names:
        values = [float(vector[feature]) for vector in vectors]
        mean = sum(values) / len(values) if values else 0.0
        variance = sum((value - mean) ** 2 for value in values) / len(values) if values else 0.0
        stats[feature] = {
            'mean': mean,
            'std': math.sqrt(variance) or 1.0,
        }

    raw_scores = [anomaly_raw_score(vector, stats, feature_names) for vector in vectors]
    sorted_scores = sorted(raw_scores)
    percentile_index = max(0, min(len(sorted_scores) - 1, int(len(sorted_scores) * 0.90))) if sorted_scores else 0
    threshold = max(1.0, sorted_scores[percentile_index] if sorted_scores else 1.0)

    return {
        'algorithm': 'Unsupervised Z-Score Anomaly Detection',
        'version': 'ml-anomaly-v2',
        'features': feature_names,
        'stats': stats,
        'threshold': threshold,
        'training_rows': len(rows),
    }


def anomaly_raw_score(vector, stats, feature_names):
    if not feature_names:
        return 0.0
    total = 0.0
    for feature in feature_names:
        feature_stats = stats[feature]
        total += abs((float(vector[feature]) - feature_stats['mean']) / feature_stats['std'])
    return total / len(feature_names)


def score_ml_anomaly(row, model):
    vector = transaction_features(row)
    feature_names = model['features']
    raw_score = anomaly_raw_score(vector, model['stats'], feature_names)
    threshold = float(model['threshold'] or 1.0)
    anomaly_score = min(100, round((raw_score / threshold) * 100, 2)) if threshold else 0
    is_anomaly = raw_score >= threshold
    reasons = []

    for feature in feature_names:
        feature_stats = model['stats'][feature]
        z_score = abs((float(vector[feature]) - feature_stats['mean']) / feature_stats['std'])
        if z_score >= 1.5:
            reasons.append(f"ML anomaly: unusual {feature.replace('_', ' ')}")

    return {
        'ml_model': model['algorithm'],
        'ml_anomaly_score': anomaly_score,
        'ml_raw_score': round(raw_score, 4),
        'ml_prediction': 'Anomaly' if is_anomaly else 'Normal',
        'ml_confidence': min(99, round(55 + anomaly_score * 0.44, 2)) if is_anomaly else max(50, round(100 - anomaly_score * 0.35, 2)),
        'ml_reasons': reasons or ['ML pattern is close to learned normal behavior'],
    }
