from ..entities.namespace import Namespace

import autogen
import chromadb

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

class Session:

    namespace: Namespace = None

    messages: list[dict] = []

    def __init__(self, modules, pdf_path, openai_api_key, openai_api_base, openai_model,planner_system, operator_system,user_system):
        self.namespace = Namespace(modules)
        #print('self.namespace.functions_list()',self.namespace.functions_list)
        self.func_list,self.func_map=self.namespace.functions_list
        self.pdf_path = pdf_path
        self.openai_api_key = openai_api_key
        self.openai_api_base = openai_api_base
        self.openai_model = openai_model
        self.planner_system = planner_system
        self.operator_system = operator_system
        self.user_system = user_system

        self.config_list=[
            {
                "model": self.openai_model,
                'api_key': self.openai_api_key,
                'base_url': self.openai_api_base,
            }
        ]

        self.llm_config_planner = {
            # "Seed": 42,
            "temperature": 0,
            "config_list": self.config_list,
            "timeout": 600,
        }
        self.llm_config_operator={
            "temperature": 0,
            "functions":self.func_list,
            "config_list": self.config_list,
            "timeout": 600,
        }

        self.llm_config = {"config_list": self.config_list, "cache_seed": 42}
        from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
        import time
        self.retrieve_user_proxy = RetrieveUserProxyAgent(
            name="user",
            is_termination_msg=termination_msg,
            system_message=self.user_system,
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=1000,
            retrieve_config={
                "task": "qa",
                "model":self.openai_model,
                "docs_path": self.pdf_path,
                "custom_text_types": ["mdx"],
                "chunk_token_size": 20000,
                "vector_db": "chroma",
                "overwrite": False,  # set to True if you want to overwrite an existing collection
                "get_or_create": True,  # set to False if don't want to reuse an existing collection
                "update_context": False
            },
            
            # retrieve_config={
            #     "task": "qa",
            #     "docs_path": self.pdf_path,
            #     "chunk_token_size": 2000,
            #     "model": self.openai_model,
            #     "client": chromadb.PersistentClient(path="/tmp/chromadb"),
            #     "collection_name": "2wikimultihopqa",
            #     "chunk_mode": "one_line",
            #     "embedding_model": "all-MiniLM-L6-v2",
            #     "customized_prompt": PROMPT_MULTIHOP,
            #     "customized_answer_prefix": "the answer is",
            # },
            
            # retrieve_config={
            #     "task": "qa",
            #     "docs_path": self.pdf_path,
            #     "chunk_token_size": 2000,
            #     "model": self.openai_model,
            #     "client": chromadb.PersistentClient(path="/tmp/chromadb"),
            #     "collection_name": "natural-questions",
            #     "chunk_mode": "one_line",
            #     "embedding_model": "all-MiniLM-L6-v2",
            # },
            code_execution_config=False,  # we don't want to execute code in this case.
            function_map=self.func_map

        )
        #print('llm_config_operator.functions', self.llm_config_operator['functions'])
        #print('retrieve_user_proxy.func map', self.retrieve_user_proxy.function_map)
        self.planner = autogen.AssistantAgent(
            name="planner",
            llm_config=self.llm_config_planner,
            system_message=self.planner_system,
            is_termination_msg=termination_msg
        )

        self.operator = autogen.AssistantAgent(
            name="operator",
            llm_config=self.llm_config_operator,
            system_message=self.operator_system,
            is_termination_msg=termination_msg
        )
        # self.groupchat = autogen.GroupChat(agents=[self.retrieve_user_proxy, self.planner, self.operator], messages=[], max_round=1200)
        self.groupchat = autogen.GroupChat(agents=[self.retrieve_user_proxy, 
                                                   self.planner, self.operator], 
                                           messages=[], 
                                           max_round=200, 
                                           speaker_selection_method='round_robin'
                                           )
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, 
                                                llm_config=self.llm_config,
                                                is_termination_msg=termination_msg)
    def ask(self, task_des):
        self.retrieve_user_proxy.initiate_chat(self.manager, 
                                               message=self.retrieve_user_proxy.message_generator,
                                               problem=task_des)
        print(self.retrieve_user_proxy.chat_messages)
        self.retrieve_user_proxy.chat_messages
        self.retrieve_user_proxy.chat_messages
        return_message = '任务执行完成!'
        
        return return_message
