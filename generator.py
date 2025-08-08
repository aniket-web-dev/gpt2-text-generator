from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class GPT2TextGenerator:
    def __init__(self, model_name='gpt2'):
        print("Loading model and tokenizer...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        if torch.cuda.is_available():
            self.model.to('cuda')
            print("Using GPU acceleration.")
        else:
            print("GPU not detected, using CPU.")

    def generate_text(self, prompt, max_length=100, num_return_sequences=1, temperature=1.0):
        # Encode input prompt
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to('cuda')
        # Generate outputs
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        # Decode and return the text
        generated_texts = [self.tokenizer.decode(out, skip_special_tokens=True) for out in outputs]
        return generated_texts
