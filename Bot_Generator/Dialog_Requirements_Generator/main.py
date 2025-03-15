#!/usr/bin/env python3
import os
import sys
import csv
import yaml
from utils import str_to_bool, sanitize_filename, process_answer, split_by_sep
from build_samples_list import build_samples_list

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print(f"  {os.path.basename(sys.argv[0])} dialogs.csv output_dir")
        sys.exit(1)
    
    dialogs_csv = sys.argv[1]
    output_dir = sys.argv[2]

    base_dialogs_path = os.path.join(output_dir, "dialogs")
    os.makedirs(base_dialogs_path, exist_ok=True)

    dialogs_data = []
    topics_set = set()

    with open(dialogs_csv, newline="", encoding="utf-8") as df:
        reader = csv.DictReader(df)
        for row in reader:
            topic_val = row.get("Topic", "").strip()
            name_val = row.get("Name", "").strip()
            answer_val = row.get("Answer", "").strip()
            if not topic_val or not name_val or not answer_val:
                continue
            rec = {
                "Topic": topic_val,
                "Name": name_val,
                "Answer": answer_val,
                "Description": row.get("Description", "").strip(),
                "Active": row.get("Active", "").strip(),
                "Title": row.get("Title", "").strip(),
                "Payload": row.get("Payload", "").strip(),
                "Conditions": row.get("Conditions", "").strip(),
                "Required_variables": row.get("Required_variables", "").strip(),
                "Start_actions": row.get("Start_actions", "").strip(),
                "End_actions": row.get("End_actions", "").strip(),
                "Samples": row.get("Samples", "").strip(),
                "Intent": row.get("Intent", "").strip()
            }
            dialogs_data.append(rec)
            topics_set.add(topic_val)

    topics_dict = {}
    for t in sorted(topics_set, key=lambda x: x.lower()):
        topics_dict[t.lower()] = {"name": t}
    if not topics_dict:
        topics_dict["other"] = {"name": "Other"}

    final_topics = {"topics": topics_dict}
    topics_file = os.path.join(output_dir, "topics.yaml")
    with open(topics_file, "w", encoding="utf-8") as tf:
        yaml.dump(final_topics, tf,
                  sort_keys=False,
                  allow_unicode=True,
                  width=9999,
                  default_flow_style=False)
    print(f"Created topics.yaml at '{topics_file}'.")

    created_topic_folders = set()
    for d in dialogs_data:
        topic_raw = d["Topic"]
        topic_lower = topic_raw.lower() if topic_raw else "other"
        topic_original = topic_raw if topic_raw else "Other"

        topic_folder = os.path.join(base_dialogs_path, topic_lower)
        if topic_folder not in created_topic_folders:
            os.makedirs(topic_folder, exist_ok=True)
            created_topic_folders.add(topic_folder)

        dialog_name = d["Name"]
        desc = d["Description"]
        active_val = str_to_bool(d["Active"])
        fname_core = sanitize_filename(dialog_name)
        raw_answer = process_answer(d["Answer"], 120)

        button_list = split_by_sep(d["Title"], ";")
        payload_list = split_by_sep(d["Payload"], ";")
        cond_list = split_by_sep(d["Conditions"], ";")
        reqv_str = d["Required_variables"]
        reqv_data = {} if not reqv_str else {}
        start_list = split_by_sep(d["Start_actions"], ";")
        end_list = split_by_sep(d["End_actions"], ";")
        samples_list = build_samples_list(d["Samples"], d["Intent"])

        answers_array = []
        answer_obj = {"text": raw_answer} if raw_answer else {}

        if button_list:
            answer_obj["buttons"] = [
                {"title": button_list[i], "payload": payload_list[i] if i < len(payload_list) else ""}
                for i in range(len(button_list))
            ]

        if cond_list:
            answer_obj["conditions"] = cond_list

        answers_array.append(answer_obj)

        dialogs_block = {
            dialog_name: {
                "name": dialog_name,
                "topic": topic_lower,
                "active": active_val,
                "start_actions": start_list,
                "end_actions": end_list,
                "answers": answers_array,
                "required_variables": reqv_data,
                "samples": samples_list
            }
        }
        if desc:
            dialogs_block[dialog_name]["description"] = desc

        final_yaml = {"dialogs": dialogs_block}
        out_file = os.path.join(topic_folder, f"{fname_core}.yaml")
        with open(out_file, "w", encoding="utf-8") as outf:
            yaml.dump(final_yaml, outf,
                      sort_keys=False,
                      allow_unicode=True,
                      width=9999,
                      default_flow_style=False)
        print(f"Created dialog file: {out_file}")

    print(f"Done! Dialogs are created under '{base_dialogs_path}' and topics.yaml is at '{topics_file}'.")

if __name__ == "__main__":
    main()
