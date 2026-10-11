def compare_metrics(metrics_a, metrics_b):
    
    comparison = {}

    for key in metrics_a: 
        if key in metrics_b: 
            value_a = metrics_a[key]
            value_b = metrics_b[key]

            if isinstance(value_a, (int, float)) and isinstance(value_b, (int, float)):
                comparison[key] = {
                    "throw_a": value_a, 
                    "throw_b": value_b,
                    "comparison": value_a - value_b
                }

            elif isinstance(value_a, (str)) and isinstance(value_b, (str)):
                comparison[key] = {
                    "throw_a": value_a, 
                    "throw_b": value_b,
                    "comparison": value_a != value_b
                }


    
    return comparison
