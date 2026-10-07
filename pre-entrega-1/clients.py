from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional
import os
import openai
from openai import AsyncOpenAI
import anthropic
from anthropic import AsyncAnthropic

from schemas import ChatMessage, ModelConfig, ModelResponse

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> ModelResponse:
        pass

    @abstractmethod
    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        pass

class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> ModelResponse:
        try:
            formatted = [{"role": m.role, "content": m.content} for m in messages]
            response = await self.client.chat.completions.create(
                model=config.model,
                messages=formatted,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            choice = response.choices[0].message
            usage = response.usage.total_tokens if response.usage else None
            return ModelResponse(
                content=choice.content or "",
                model=response.model,
                tokens_used=usage
            )
        except (openai.RateLimitError, openai.APIConnectionError, openai.APIError) as e:
            return ModelResponse(
                content="",
                model=config.model,
                error=f"Error en OpenAI: {e}"
            )
        except Exception as e:
            return ModelResponse(
                content="",
                model=config.model,
                error=f"Error inesperado: {e}"
            )

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        try:
            formatted = [{"role": m.role, "content": m.content} for m in messages]
            response = await self.client.chat.completions.create(
                model=config.model,
                messages=formatted,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                stream=True
            )
            async for chunk in response:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    yield delta
        except (openai.RateLimitError, openai.APIConnectionError, openai.APIError) as e:
            yield f"\n[Error de OpenAI: {e}]"
        except Exception as e:
            yield f"\n[Error inesperado: {e}]"

class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    def _split_system_message(self, messages: List[ChatMessage]):
        system_text = ""
        user_assistant_msgs = []
        for m in messages:
            if m.role == "system":
                system_text += f"{m.content}\n"
            else:
                user_assistant_msgs.append({"role": m.role, "content": m.content})
        return system_text.strip() or None, user_assistant_msgs

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> ModelResponse:
        try:
            system, chat_msgs = self._split_system_message(messages)
            model_name = config.model if "claude" in config.model else "claude-3-haiku-20240307"
            kwargs = {
                "model": model_name,
                "messages": chat_msgs,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
            }
            if system:
                kwargs["system"] = system

            response = await self.client.messages.create(**kwargs)
            text = "".join([block.text for block in response.content if hasattr(block, "text")])
            usage = response.usage.input_tokens + response.usage.output_tokens if response.usage else None
            return ModelResponse(
                content=text,
                model=response.model,
                tokens_used=usage
            )
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APIError) as e:
            return ModelResponse(
                content="",
                model=config.model,
                error=f"Error en Anthropic: {e}"
            )
        except Exception as e:
            return ModelResponse(
                content="",
                model=config.model,
                error=f"Error inesperado: {e}"
            )

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        try:
            system, chat_msgs = self._split_system_message(messages)
            model_name = config.model if "claude" in config.model else "claude-3-haiku-20240307"
            kwargs = {
                "model": model_name,
                "messages": chat_msgs,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
            }
            if system:
                kwargs["system"] = system

            async with self.client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APIError) as e:
            yield f"\n[Error de Anthropic: {e}]"
        except Exception as e:
            yield f"\n[Error inesperado: {e}]"

class AsyncLLMManager:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider.lower()
        if self.provider == "openai":
            self.client: BaseLLMClient = OpenAIClient(api_key=api_key)
        elif self.provider == "anthropic":
            self.client = AnthropicClient(api_key=api_key)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> ModelResponse:
        return await self.client.generate(messages, config)

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        async for chunk in self.client.stream(messages, config):
            yield chunk
