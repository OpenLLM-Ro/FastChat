# Evaluation of RoLLMs

Official code used for evaluating Romanian LLMs as proposed in [Masala et al. 2024](https://arxiv.org/abs/2406.18266). This repo is a fork of the popular [FastChat](https://github.com/lm-sys/FastChat) repo used for LLM-as-a-Judge evaluation. On top of the existing framework we add a suite of Romanian benchmarks:

- RoMTBench - the manually translated version of MTBench in Romanian
- RoCulturaBench - a novel professionaly designed and built dataset for evaluating Romanian cultural knowledge of LLMs


The questions and (human) answers for RoMTBench and RoCulturaBench can be found [here](https://github.com/denisilie94/FastChat/tree/main/fastchat/llm_judge/data/mt_bench_ro) and [here](https://github.com/denisilie94/FastChat/tree/main/fastchat/llm_judge/data/cultura_bench_ro) respectively.

Models answers and judgments will be uploaded soon.


## Evaluation
For evaluating LLMs using (Ro)MTBench and RoCulturaX please see [fastchat/llm_judge](fastchat/llm_judge).

## Citation

```bibtex
@inproceedings{masala-etal-2024-vorbesti,
    title = "``Vorbe\c{s}ti Rom{\^a}ne\c{s}te?'' A Recipe to Train Powerful {R}omanian {LLM}s with {E}nglish Instructions",
    author = "Masala, Mihai and Ilie-Ablachim, Denis and Dima, Alexandru and Corlatescu, Dragos Georgian and Zavelca, Miruna-Andreea and Olaru, Ovio and Terian, Simina-Maria and Terian, Andrei and Leordeanu, Marius and Velicu, Horia and Popescu, Marius and Dascalu, Mihai and Rebedea, Traian",
    editor = "Al-Onaizan, Yaser and Bansal, Mohit and Chen, Yun-Nung",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.681/",
    doi = "10.18653/v1/2024.findings-emnlp.681",
    pages = "11632--11647"
}
```

### Acknowledgement
This repo benefits from [FastChat](https://github.com/lm-sys/FastChat). We thank them for their wonderful work.
