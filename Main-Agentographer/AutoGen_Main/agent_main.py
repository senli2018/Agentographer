# 智能体的角色定义，整体agent的架构启动都在这里

import importlib
import logging
from openai_key import api_key, base_url
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# 程序运行前需要设置环境变量
# set HF_ENDPOINT=https://hf-mirror.com

class group1():
    def __init__(self) -> None:
        modules = [
                    'agent_toolbox.py'
                    ]
        pdf_path='ct_group/docs_lisen_copy.txt'
        openai_api_key=api_key
        openai_api_base=base_url
        # openai_model="gpt-3.5-turbo"
        openai_model="gpt-4o"
        # llama3-8b-8192、llama3-groq-8b-8192-tool-use-preview、meta-llama/Llama-3.2-90B-Vision-Instruct、llama3-70b-8192、llama-3.3-70b-versatile、llama-3.2-90b-vision-preview、llama-3.2-3b-preview、llama-3.2-1b-preview、llama-3.2-11b-vision-preview、llama-3.1-8b-instant、llama-3.1-70b-versatile
        #llama-3.1-70b、llama-3.1-405b-instruct、aihubmix-Llama-3-70B-Instruct、aihubmix-Llama-3-2-90B-Vision
        # openai_model = "llama-3.1-405b-instruct"

        planner_system = "你是一个优秀的CT成像专家，你基于user给定的文档内容和任务问题，完成CT操作。你接受user的计划指令，严格按照user的指令，必须根据指令重新规划任务并指挥operator执行调用。"
        operator_system="你是一个优秀的CT操作专家，请你调用API, 将planner提供的操作序列必须完整运行后才结束。"
        user_system = "你是monitor角色，你可以根据实际CT间状况向planer反馈应该调用的命令。"

        self.messeges = []

        imported_modules = []

        for module_name in modules:
            #print('module_name: ', module_name)
            module_name = module_name.replace("/", ".").replace("\\", ".")
            if module_name.endswith('.py'):
                module_name = module_name[:-3]
            module = importlib.import_module(module_name)
            #print("Using module: {}".format(module.__name__))
            imported_modules.append(module)
        if len(imported_modules) == 0:
            logging.warning("No module imported, you're in normal chat mode.")
        #print(imported_modules)
        from ct_group.agentSession.session.session import Session
        self.session = Session(modules=imported_modules,
                               pdf_path=pdf_path,
                               openai_api_key=openai_api_key,
                               openai_api_base=openai_api_base,
                               openai_model=openai_model,
                               planner_system=planner_system,
                               operator_system=operator_system,
                               user_system=user_system)

    def autoGEN_clone(self, input, history):
        history = history or []
        s = list(sum(history, ()))
        s.append(input)
        msg={"role": "user", "content": input}
        self.messeges.append(msg)
        #inp = ' '.join(s)
        output = self.session.ask(input)
        msg={"role": "assistant", "content": output}
        self.messeges.append(msg)
        print('output_msgs',self.messeges)
        history.append((input, output))
        return history

if __name__ == "__main__":
    group = group1()
    group.autoGEN_clone(input="请根据CT拍摄流程，为患者拍摄肺部CT", history=[])


