# Vojta
A tool to convert SMILES to IUPAC notation using character-based transformer neural network.
Under the hood it uses a transformer to generate the output sequence character at a time.
The architecture of the transformer is exactly the one from the attention is all you need paper.
The model has been trained on around 300 000 samples for 8 hours on 1x A100 GPU on google colab, achieveing 75% accuracy.
This is less than the state of the art and could likely be improved by getting more training data.
The model weights are in the model_weights.pt file
