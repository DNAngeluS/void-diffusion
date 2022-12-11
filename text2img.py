import torch, os, time, datetime, colab, postprocessor, progress, importlib
from IPython.display import display
importlib.reload(postprocessor)

def process(ShouldSave):
    if 'Seed' not in colab.settings: "Please set your settings first."
    colab.settings['Seed'] = torch.random.seed() if colab.settings['Seed'] == 0 else colab.settings['Seed']
    generator = torch.Generator("cuda").manual_seed(colab.settings['Seed'])
    # how to get the image every 100 steps in StableDiffusionPipeline?
    images = colab.text2img(
        width=colab.settings['Width'],
        height=colab.settings['Height'],
        prompt=colab.settings['Prompt'],
        negative_prompt=colab.settings['NegativePrompt'],
        guidance_scale=colab.settings['GuidanceScale'],
        num_inference_steps=colab.settings['Steps'],
        generator=generator,
        callback=progress.callback,
        callback_steps=10).images
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    if ShouldSave:
        if colab.save_settings: postprocessor.save_settings(timestamp)
        for i, image in images:
            imageName = timestamp + "_" + str(i)
            print(imageName)
            path = postprocessor.save_gdrive(image, imageName)
            display(image, str(i))
            print("Saved to " + path)
            postprocessor.post_process(image, imageName)