import os, json, shutil, requests, numpy as np
from manim import *
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
with open('daily_params.json', 'r') as f:
    daily_data = json.load(f)
class FreshKineticMotion(Scene):
    def __init__(self, index, **kwargs):
        self.index = index
        self.params = daily_data['palettes'][index]
        self.seed = daily_data['seeds'][index]
        super().__init__(**kwargs)
    def construct(self):
        np.random.seed(self.seed)
        p = self.params
        bg = FullScreenRectangle().set_fill(color=[p[0], p[1]], opacity=1)
        self.add(bg)
        strips = VGroup()
        for i in range(15):
            strip = Rectangle(width=16, height=0.5, fill_color=p[i%4], fill_opacity=0.4)
            strip.move_to([np.random.uniform(-4, 4), np.random.uniform(-3, 3), 0])
            strips.add(strip)
        self.add(strips)
        self.play(*[s.animate.shift(RIGHT*4) for s in strips], run_time=10, rate_func=linear)
if __name__ == "__main__":
    output_folder = "render_output"
    os.makedirs(output_folder, exist_ok=True)
    for i in range(20):
        scene = FreshKineticMotion(index=i)
        scene.render()
        mp4_path = [os.path.join(r, f) for r, d, fs in os.walk("./media") for f in fs if f.endswith(".mp4")][0]
        out_name = f"Motion_4K_V2_{i+1}.mov"
        final_out = os.path.join(output_folder, out_name)
        os.system(f"ffmpeg -y -i {mp4_path} -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le {final_out}")
        with open(final_out, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", data={"chat_id": CHAT_ID, "caption": f"Variant {i+1} DONE"}, files={"document": f})
        shutil.rmtree("./media")
        os.remove(final_out)
