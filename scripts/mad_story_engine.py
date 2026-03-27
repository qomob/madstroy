import json
import os

class MadStoryEngine:
    def __init__(self, assets_path, references_path):
        self.assets_path = assets_path
        self.references_path = references_path
        self.current_state = {
            "phase": 1,
            "concept": "",
            "timeline": "",
            "composition": "",
            "camera": "",
            "lighting": "",
            "sound": "",
            "duration": 15,
            "params": {}
        }
        self.load_resources()

    def load_resources(self):
        with open(os.path.join(self.assets_path, 'cheat_sheet.json'), 'r', encoding='utf-8') as f:
            self.cheat_sheet = json.load(f)

    def next_phase(self, user_input):
        if self.current_state["phase"] == 1:
            self.current_state["concept"] = user_input
            self.current_state["phase"] = 2
            return "核心创意已锁定。现在请规划 **15 秒时间轴**：请简单描述这 15 秒内的节奏变化（例如：0-5秒入场，5-12秒核心动作，12-15秒收尾）。"
        
        elif self.current_state["phase"] == 2:
            self.current_state["timeline"] = user_input
            self.current_state["phase"] = 3
            return "时间轴已记录。现在进入 **视觉构图**：你希望画面比例是多少？角色在画面中的位置（三分法、中心构图）？"

        elif self.current_state["phase"] == 3:
            self.current_state["composition"] = user_input
            self.current_state["phase"] = 4
            return "构图已定。接下来是 **动态运镜**：请描述镜头运动，最好能对应到秒（例如：前5秒推镜头，后10秒环绕镜头）。"

        elif self.current_state["phase"] == 4:
            self.current_state["camera"] = user_input
            self.current_state["phase"] = 5
            return "镜头语言已记录。现在是 **光影与细节**：想要什么样的色调和光效（如：赛博朋克、黑白电影、霓虹灯光）？"

        elif self.current_state["phase"] == 5:
            self.current_state["lighting"] = user_input
            self.current_state["phase"] = 6
            return "氛围感拉满了。最后，**声音设计**：15秒内的音乐或音效节奏如何规划？"

        elif self.current_state["phase"] == 6:
            self.current_state["sound"] = user_input
            self.current_state["phase"] = 7
            return self.generate_final_output()

    def generate_final_output(self):
        # 优化提示词生成逻辑，体现 15 秒和逐秒级构思
        prompt = f"Cinematic 15s shot: {self.current_state['concept']}. " \
                 f"Timeline rhythm: {self.current_state['timeline']}. " \
                 f"Composition: {self.current_state['composition']}. " \
                 f"Second-by-second camera: {self.current_state['camera']}. " \
                 f"Lighting: {self.current_state['lighting']}. " \
                 f"Vibe: high quality, 4k, seedance 2.0 style, --duration 15s."
        
        output = {
            "STANDARD_PROMPT": prompt,
            "TIMELINE": self.current_state['timeline'],
            "CAMERA_MOVEMENT": self.current_state['camera'],
            "MOTION_STRENGTH": 5,
            "DURATION": "15s",
            "IMAGE_REF_ADVICE": "建议上传一张具有相似色调和构图的高质量图像作为参考",
            "VIBE_ADVICE": self.current_state['lighting'],
            "SOUND_DESIGN": self.current_state['sound']
        }
        
        return output

    def render_to_html(self, output):
        with open(os.path.join(self.assets_path, 'storyboard_template.html'), 'r', encoding='utf-8') as f:
            template = f.read()
        
        for key, value in output.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        return template

if __name__ == "__main__":
    # 示例运行
    assets = "/Users/jonki/.trae/skills/mad-story/assets"
    refs = "/Users/jonki/.trae/skills/mad-story/references"
    engine = MadStoryEngine(assets, refs)
    
    print("Welcome to MadStory!")
    # 这里只是为了演示逻辑
    # print(engine.next_phase("一个赛博朋克风格的街头武士，正在雨中行走"))
