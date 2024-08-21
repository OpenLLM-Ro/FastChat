import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import numpy as np
import argparse
import re


CATEGORIES_MT = ["Writing", "Roleplay", "Extraction", "Math", "Coding", "Reasoning", "Stem", "Humanities"]
CATEGORIES_SB = ["Writing", "Role", "Argumentation", "Geography", "History", "Culture&Sciene", "Sport", "Customs&Traditions", "Stereotypes", "Celebrity"]


MODEL_JUDGMENT_PATH = "data/mt_bench_ro/model_judgment/gpt-4o-2024-05-13_single.jsonl"


def get_model_df(dataset_name):
    if "mt_bench" in dataset_name:
        x = 81
        categs = CATEGORIES_MT
    elif dataset_name == "":
        x = 0
        categs = CATEGORIES_SB
        
    q2result = []
    fin = open(MODEL_JUDGMENT_PATH, "r", encoding="utf-8")
    for line in fin:
        obj = json.loads(line)
        obj["category"] = categs[(obj["question_id"]-x)//10]
        q2result.append(obj)
    df = pd.DataFrame(q2result)
    return df



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
    args = parser.parse_args()


    df = get_model_df(args.bench_name)

    all_models = df["model"].unique()

    if args.model_list is not None:
        if len(args.model_list) == 1 and args.model_list[0].startswith("*"):
            if "llama" in args.model_list[0] and "-" not in args.model_list[0]:
                models = list(filter(lambda x: args.model_list[0][1:] in x.lower() or args.model_list[0][1:-1]+"-"+args.model_list[0][-1] in x.lower(), all_models))
            else:
                models = list(filter(lambda x: args.model_list[0][1:].lower() in x.lower(), all_models))
        else:
            models = args.model_list
            df = df[df["model"].isin(args.model_list)]
    else:
        models = all_models
    
    scores_all = []
    scores_ft = []
    scores_st = []
    for model in models:
        full_scores = []

        for cat in CATEGORIES_MT:            
            res = df[(df["category"]==cat) & (df["model"]==model) & (df["score"] >= 0)]
            score = res["score"].mean()
            full_scores.extend(list(res["score"]))
            scores_all.append({"model": model, "category": cat, "score": score})

            res = df[(df["category"]==cat) & (df["model"]==model) & (df["turn"] == 1)]
            score = res["score"].mean()
            scores_ft.append(({"model": model, "category": cat, "score": score}))

            res = df[(df["category"]==cat) & (df["model"]==model) & (df["turn"] == 2)]
            score = res["score"].mean()
            scores_st.append(({"model": model, "category": cat, "score": score}))

    save_path = 'detailed_scores/'
    os.makedirs(save_path, exist_ok=True)

    with open(os.path.join(save_path, "per_categ_global"), 'w') as file:
        for entry in scores_all:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

    with open(os.path.join(save_path, "per_categ_first_turn"), 'w') as file:
        for entry in scores_ft:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

    with open(os.path.join(save_path, "per_categ_second_turn"), 'w') as file:
        for entry in scores_st:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

    for index, scores_to_consider in enumerate([scores_all, scores_ft, scores_st]):
        if index == 0:
            name = "Global"
        elif index == 1:
            name = "First turn"
        else:
            name = "Second turn"
        target_models = list(all_models)
        scores_target = [scores_to_consider[i] for i in range(len(scores_to_consider)) if scores_to_consider[i]["model"] in target_models]
        # sort by target_models
        scores_target = sorted(scores_target, key=lambda x: target_models.index(x["model"]), reverse=True)
        df_score = pd.DataFrame(scores_target)
        df_score = df_score[df_score["model"].isin(target_models)]
        fig = px.line_polar(df_score, r = 'score', theta = 'category', line_close = True, category_orders = {"category": CATEGORIES_MT},
                            color = 'model', markers=True, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig['layout']['title'] = name
        fig.show()
        fig.update_layout(font=dict(size=18,),)
        fig.write_image(os.path.join(save_path, "{0}.png".format(name.replace(" ", "_"))), width=800, height=600, scale=2)