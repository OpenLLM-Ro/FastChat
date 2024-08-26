# Evaluation of RoLLMs

Official code used for evaluating Romanian LLMs as proposed in [Masala et al. 2024](https://arxiv.org/abs/2406.18266). This repo is a fork of the popular [FastChat](https://github.com/lm-sys/FastChat)) repo used for LLM-as-a-Judge evaluation. On top of the existing framework we add a suite of Romanian benchmarks:

- RoMTBench - the manually translated version of MTBench in Romanian
- RoCulturaBench - a novel professionaly designed and built dataset for evaluating Romanian cultural knowledge of LLMs


The questions and (human) answers for RoMTBench and RoCulturaBench can be found [here](https://github.com/denisilie94/FastChat/tree/main/fastchat/llm_judge/data/mt_bench_ro) and [here](https://github.com/denisilie94/FastChat/tree/main/fastchat/llm_judge/data/cultura_bench_ro) respectively.

Models answers and judgments will be uploaded soon.


## Evaluation
For evaluating LLMs using (Ro)MTBench and RoCulturaX please see [fastchat/llm_judge](fastchat/llm_judge).

## Cite as

```bibtex
@misc{masala2024vorbecstiromanecsterecipetrain,
      title={"Vorbe\c{s}ti Rom\^ane\c{s}te?" A Recipe to Train Powerful Romanian LLMs with English Instructions}, 
      author={Mihai Masala and Denis C. Ilie-Ablachim and Alexandru Dima and Dragos Corlatescu and Miruna Zavelca and Ovio Olaru and Simina Terian and Andrei Terian and Marius Leordeanu and Horia Velicu and Marius Popescu and Mihai Dascalu and Traian Rebedea},
      year={2024},
      eprint={2406.18266},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2406.18266}, 
}
```

### Acknowledgement
This repo benefits from [FastChat](https://github.com/lm-sys/FastChat). We thank them for their wonderful work.
