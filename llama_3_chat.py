import replicate

# The meta/meta-llama-3-70b-instruct model can stream output as it's running.
for event in replicate.stream(
    "meta/meta-llama-3-70b-instruct",
    input={
        "prompt": "Can you write a poem about open source machine learning?"
    },
):
    print(str(event), end="")
