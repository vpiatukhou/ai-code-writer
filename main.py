from transformers import AutoTokenizer, AutoModelForCausalLM
import tools
import json

_MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
_CACHE_DIR = './models/huggingface-cache'

tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME, cache_dir=_CACHE_DIR)
model = AutoModelForCausalLM.from_pretrained(_MODEL_NAME, device_map="auto", cache_dir=_CACHE_DIR)
messages = [
    {"role": "system", "content": tools.PROMPT},
	{"role": "user", "content": ""},
]

while True:
    print("Запрос принят.")

    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=1024)
    output_text = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])

    messages.append({"role": "assistant", "content": output_text})

    try:
        output_json = json.loads(output_text)
        tool_spec = output_json["tool_call"]
        tool_result = tools.call_tool(tool_spec)
    except Exception:
        print(output_text)
        print("Диалог завершен.")
        break

    messages.append({"role": "tool", "content": tool_result})
