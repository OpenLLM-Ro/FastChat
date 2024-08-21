import json
import time
import sys
import os
import copy

import argparse


from nltk.tokenize import sent_tokenize
from langdetect import detect, LangDetectException, DetectorFactory, detect_langs


# Ensure that the NLTK package is installed
# nltk.download('punkt')

DetectorFactory.seed = 0
LANG_REF = 'ro'
OUTFILE = "lang_counter.info"

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            # Load each line as a JSON object
            data.append(json.loads(line))
    return data


def detect_language_distribution(text):
    # Split text into sentences
    sentences = sent_tokenize(text)
    
    # Dictionary to hold language counts
    language_counts = {}
    
    # Detect language for each sentence and count occurrences
    for sentence in sentences:
        try:
            language = detect(sentence)
            if language in language_counts:
                language_counts[language] += 1
            else:
                language_counts[language] = 1
        except LangDetectException:
            continue
    
    # Total number of sentences
    total_sentences = sum(language_counts.values())
    
    # Calculate percentage of each language
    language_percentages = {lang: (count / total_sentences * 100.0) for lang, count in language_counts.items()}
    
    return language_percentages


def get_dominant_language(language_percentages):
    if not language_percentages:
        return None

    # Find the maximum value
    max_value = max(language_percentages.values())
    
    # Find all keys with the maximum value
    max_keys = [k for k, v in language_percentages.items() if v == max_value]
    
    # Check if 'ro' is one of the keys with the maximum value
    if 'ro' in max_keys:
        return 'ro'
    else:
        return max_keys[0]




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--bench-name", type=str, default="mt_bench_ro")
    parser.add_argument(
        "--model-list",
        type=str,
        nargs="+",
        default=None,
        help="A list of models to be evaluated",
    )
    parser.add_argument("--show_all", action="store_true")
    
    args = parser.parse_args()


    ANSWERS_PATH = "./data/{0}/model_answer/".format(args.bench_name)
    JUDGMENTS_PATH = "./data/{0}/model_judgment/".format(args.bench_name)

    if args.model_list[0] == "all":
        args.model_list = os.listdir(ANSWERS_PATH)
        args.model_list = list(map(lambda x: x[:-6], args.model_list))
    args.model_list = args.model_list[:2]


    judgments = {}
    for jf in os.listdir(JUDGMENTS_PATH):
        data = read_jsonl(os.path.join(JUDGMENTS_PATH, jf))
        judgments[jf] = data

    with open(OUTFILE, "w", encoding="utf-8") as logfile:
        for model in args.model_list:
            data = read_jsonl(os.path.join(ANSWERS_PATH, model+".jsonl"))
            counter = 0
            total = 0
            for item in data:
                for turn_index, turn in enumerate(item['choices'][0]['turns']):
                    total += 1
                    try:
                        language_percentages = detect_language_distribution(turn)
                        lang = get_dominant_language(language_percentages)
                        lp = detect_langs(turn)
                    except:
                        print('langdetect error - returning empty lang')
                        lang = ''

                    if lang == LANG_REF:
                        counter += 1
                    else:
                        write_to_file = False
                        for k, v in judgments.items():
                            judgment = v
                            og_judgment = copy.deepcopy(judgment)
                            # search for question
                            judgment = list(filter(lambda x: x["question_id"] == item["question_id"] and x["model"] == model, judgment))
                            if turn_index == 0:
                                judgment = list(filter(lambda x: x["judge"][1] in ["single-v1", "single-math-v1"], judgment))
                            else:
                                judgment = list(filter(lambda x: x["judge"][1] in ["single-v1-multi-turn", "single-math-v1-multi-turn"], judgment))
                            
                            if len(judgment) > 1:
                                print("More than one judgment for model {0}, question {1}, turn {2}.".format(model, item["question_id"], turn_index+1))
                                sys.exit()
                            if len(judgment) == 0:
                                logfile.write("Model {0} has not been judged by {1}.".format(model, k))
                                continue
                            score = judgment[0]["score"]
                            if score == 0 and args.show_all == False:
                                continue
                            write_to_file = "!!!!!!!!!!!!!!!!!    For judgment {0} score is {1}! Example found at line {2}.    !!!!!!!!!!!!!!!!!\n".format(k, score, og_judgment.index(judgment[0])+1)

                        if write_to_file != False:
                            logfile.write("{0}\n".format('=' * 50))
                            logfile.write("Model: {0}\n".format(model))
                            logfile.write("Detected dominant language: {0}\n".format(str(language_percentages)))
                            logfile.write("All languages: {0}\n".format(str(lp)))
                            logfile.write("Question number: {0}. Turn number: {1}\n".format(item["question_id"], turn_index+1))
                            logfile.write(write_to_file)
                            logfile.write("####\n")
                            logfile.write("Text:\n{0}\n\n".format(turn))

            print("Model: {0} | Texts in RO: {1}/{2}".format(model, counter, total))
            print()

    print("Saved output logs in", OUTFILE)