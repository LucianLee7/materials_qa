# DARWIN ORIENTAION NOTES

# What is Darwin?
An open-source large language model (LLM) tailored for materials science based on LLaMA architectures. 

It uses natural language to process inputs, which can avoid the need for designing special input formats required for each task.

DARWIN 1.5 uses a two-stage training strategy: QA fine-tuning and multi-task learning (MTL).

The QA stage injects materials-science knowledge from scientific literature, while the MTL stage allows one model to learn multiple materials-related tasks and transfer knowledge across them.

# what data it was trained on
## QA:
The QA dataset in the first stage is derived from highly-cited scientific literature. Darwin1.5 incorporates the SciQAG-24D dataset, a question-answering (QA) dataset derived from scientific papers consists of 28k open-ended QA pairs, preserving essential knowledge from lengthy scientific texts.
## MTL:
The MTL stage uses 21 open-accessed FAIR datasets from highly cited publications in materials science. These datasets are converted into natural-language instructions for 5 classification tasks and 17 regression tasks.


# Which step of its data pipeline do you think is weakest and why?
I think the QA data construction stage may be one of the weakest parts of the pipeline.

The QA data are derived from scientific literature, so the quality of the training data really depends on the QA extraction/generation process. If the generator made mistake in understanding the source text, then generate an answer that is not fully supported by the source text, incorrect information may enter the QA dataset and affect model training.

This type of error is different from the artificial counterexamples added during training. Counterexamples are artificial constructed and controlled, but QA-generation errors are unexpected. If an incorrect QA pair is treated as a correct training example, the model may learn wrong knowledge rather than learning to reject invalid inputs.

The quality of the original scientific literature is also a limitation, since errors in the source material could propagate into the generated QA data.

In addition, the paper notes that specialized notations such as SMILES are relatively sparse in natural-language scientific documents, which may limit the model's exposure to specialized material representations.
