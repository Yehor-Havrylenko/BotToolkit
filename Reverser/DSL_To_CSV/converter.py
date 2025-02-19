#!/usr/bin/env python3
import yaml
import csv
import sys
import re

def clean_text(text):
    text = text.replace(',', '')
    text = re.sub(r'<bubble_split>', '', text)
    return text.strip()

def split_topic_and_name(full_name):
    parts = full_name.split('.', 1)
    topic = parts[0] if len(parts) > 1 else full_name
    name = parts[1] if len(parts) > 1 else full_name
    return topic, name

def parse_yaml_to_csv(yaml_file, csv_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    csv_headers = [
        "Topic", "Name", "Answer", "Description", "Active", 
        "Title", "Payload", "Conditions", "Required_variables", 
        "Start_actions", "End_actions", "Samples", "Intent"
    ]
    
    rows = []

    for dialog in data.get('dialogs', []):
        for dialog_id, content in dialog.items():
            full_name = clean_text(content.get('name', ''))
            topic, name = split_topic_and_name(full_name)
            description = clean_text(content.get('description', ''))
            active = "1"

            answers = content.get('answers', [])
            for answer in answers:
                answer_text = clean_text(answer.get('text', '').replace('\n', ' '))

                buttons = answer.get('buttons', [])
                titles = [clean_text(btn.get('title', '')) for btn in buttons]
                payloads = [clean_text(btn.get('payload', '')) for btn in buttons]

                title_str = ";".join(titles) if titles else ""
                payload_str = ";".join(payloads) if payloads else ""

                samples = content.get('samples', [])

                sample_texts = []
                if isinstance(samples, list):
                    for sample in samples:
                        if isinstance(sample, dict) and 'text' in sample:
                            sample_texts.append(clean_text(sample['text']))
                        elif isinstance(sample, str):  
                            sample_texts.append(clean_text(sample))  

                samples_str = "|".join(sample_texts) if sample_texts else ""

                conditions = ""
                required_variables = ""
                start_actions = ""
                end_actions = ""
                intent = ""

                row = [
                    topic, name, answer_text, description, active,
                    title_str, payload_str, conditions, required_variables,
                    start_actions, end_actions, samples_str, intent
                ]
                rows.append(row)

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(csv_headers)
        writer.writerows(rows)

    print(f"CSV created: {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python converter.py <input_yaml> <output_csv>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    csv_file = sys.argv[2]
    
    parse_yaml_to_csv(yaml_file, csv_file)
