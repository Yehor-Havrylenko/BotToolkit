from utils import split_by_sep

def build_samples_list(samples_str: str, intent_str: str) -> list:
    samples_list = split_by_sep(samples_str, "|")
    intent_list = split_by_sep(intent_str, "|")
    result = []
    length = min(len(samples_list), len(intent_list))
    for i in range(length):
        item = {"text": samples_list[i]}
        if intent_list[i]:
            item["intent"] = intent_list[i]
        result.append(item)
    if len(samples_list) > length:
        for s in samples_list[length:]:
            result.append({"text": s})
    return result