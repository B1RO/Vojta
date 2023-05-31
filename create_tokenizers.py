from datasets import load_dataset
from tokenizers.implementations import ByteLevelBPETokenizer

# Load the TSV dataset using Hugging Face datasets library
dataset = load_dataset('csv', sep="\t", data_files="out.tsv")
smiles_tokenizer= ByteLevelBPETokenizer()
smiles_tokenizer.train_from_iterator(dataset['train']['SMILES'], vocab_size=260, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])


iupac_tokenizer= ByteLevelBPETokenizer()
iupac_tokenizer.train_from_iterator(dataset['train']['IUPAC'], vocab_size=1000, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

iupac_tokenizer.save("iupac_tokenizer")