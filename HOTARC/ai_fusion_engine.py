from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
import concurrent.futures
import logging

class AIFusionEngine:
    def __init__(self):
        self.models = []
        logging.basicConfig(filename='ai_fusion_engine.log', level=logging.INFO)

    def add_model(self, model_name):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            model = torch.nn.DataParallel(model)
            self.models.append((tokenizer, model))
            logging.info(f"Model {model_name} added successfully.")
        except Exception as e:
            logging.error(f"Error loading model {model_name}: {e}")

    def integrate_knowledge(self, text, context):
        integrated_knowledge = ""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_model = {executor.submit(self._process_model, text, context, tokenizer, model): (tokenizer, model)
                               for tokenizer, model in self.models}
            for future in concurrent.futures.as_completed(future_to_model):
                try:
                    integrated_knowledge += future.result()
                except Exception as e:
                    logging.error(f"Error processing model: {e}")
        return integrated_knowledge

    def _process_model(self, text, context, tokenizer, model):
        try:
            inputs = tokenizer(text, return_tensors="pt")
            context_inputs = tokenizer(context, return_tensors="pt")
            inputs = {key: torch.cat((inputs[key], context_inputs[key]), dim=1) for key in inputs}
            outputs = model(**inputs)
            return self._process_outputs(outputs)
        except Exception as e:
            logging.error(f"Error in _process_model: {e}")
            return ""

    def _process_outputs(self, outputs):
        return np.mean(outputs.last_hidden_state.detach().cpu().numpy(), axis=1).tobytes()