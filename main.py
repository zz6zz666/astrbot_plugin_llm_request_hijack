# data/plugins/response_modifier/main.py
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from astrbot.api import logger

@register("response_modifier", "author", "用于劫持和修改LLM回复的插件", "1.0.0")
class ResponseModifier(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.on_llm_response(priority=100)     # 设置高优先级，确保在long_term_memory（默认优先级0）之前执行
    async def modify_response(self, event: AstrMessageEvent, resp: LLMResponse):
        # 劫持LLM回复并在开头插入"【预先劫持】"
        if resp.completion_text:
            # 修改completion_text
            resp.completion_text = f"【预先劫持】{resp.completion_text}"
            logger.info(f"已修改LLM回复: {event.unified_msg_origin}")
            
        # 注意：这里不能使用yield来发送消息，钩子只用于修改响应