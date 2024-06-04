from sklearn.metrics import classification_report


def extract_spans(ner_tags):
    spans = []
    current_span = []
    for index, tag in enumerate(ner_tags):
        if tag.startswith('B-'):
            if current_span:
                spans.append((current_span[0], index, current_span[1]))
            current_span = [index, tag[2:]]
        elif tag.startswith('I-') and current_span:
            if tag[2:] != current_span[1]:
                spans.append((current_span[0], index, current_span[1]))
                current_span = [index, tag[2:]]
        else:
            if current_span:
                spans.append((current_span[0], index, current_span[1]))
                current_span = []

    if current_span:
        spans.append((current_span[0], len(ner_tags), current_span[1]))
    return spans


def evaluate_ner(actual_data, predicted_data) -> str:
    actual_set = dict()
    predicted_set = dict()
    all_set = set()

    for i, d in enumerate(actual_data):
        for l in d["labels"]:
            key = f"{i} {l[0]} {l[1]}"
            if key not in actual_set:
                actual_set[key] = [l[2]]
            else:
                actual_set[key].append(l[2])
            all_set.add(key)
        
    for i, d in enumerate(predicted_data):
        for l in d["labels"]:
            key = f"{i} {l[0]} {l[1]}"
            if key not in predicted_set:
                predicted_set[key] = [l[2]]
            else:
                predicted_set[key].append(l[2])
            all_set.add(key)

    actual_aligned = []
    predicted_aligned = []

    for key in all_set:
        actual_aligned.append(actual_set.get(key, ["O"]))
        predicted_aligned.append(predicted_set.get(key, ["O"]))

    label2id = {"O": 0}
    for actual in actual_aligned:
        for label in actual:
            if label not in label2id:
                label2id[label] = len(label2id)
    for predicted in predicted_aligned:
        for label in predicted:
            if label not in label2id:
                label2id[label] = len(label2id)

    id2label = {v: k for k, v in label2id.items()}


    # y_true = []
    # y_pred = []
    # for actual in actual_aligned:
    #     y_true_instance = np.zeros(len(label2id), dtype=int)
    #     for true_value in actual:
    #         y_true_instance[label2id[true_value]] = 1
    #     y_true.append(y_true_instance.tolist())
    # for predicted in predicted_aligned:
    #     y_pred_instance = np.zeros(len(label2id), dtype=int)
    #     for predicted_value in predicted:
    #         y_pred_instance[label2id[predicted_value]] = 1
    #     y_pred.append(y_pred_instance.tolist())

    y_true = [
        label2id[true_value[0]]
        for true_value in actual_aligned
    ]
    y_pred = [
        label2id[predicted_value[0]]
        for predicted_value in predicted_aligned
    ]


    report = classification_report(
        y_true,
        y_pred,
        digits=4,
        target_names=[l for l in label2id.keys() if l != "O"],
        zero_division=0,
        labels=[label2id[l] for l in label2id.keys() if l != "O"],
    )

    print(report)

    return report