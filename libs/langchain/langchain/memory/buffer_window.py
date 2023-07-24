from typing import Any, Dict, List

from langchain.callbacks.manager import Callbacks
from langchain.memory.chat_memory import BaseChatMemory
from langchain.schema.messages import BaseMessage, get_buffer_string


class ConversationBufferWindowMemory(BaseChatMemory):
    """Buffer for storing conversation memory inside a limited size window."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "history"  #: :meta private:
    k: int = 5
    """Number of messages to store in buffer."""

    @property
    def buffer(self) -> List[BaseMessage]:
        """String buffer of memory."""
        return self.chat_memory.messages

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(
        self, inputs: Dict[str, Any], callbacks: Callbacks = None
    ) -> Dict[str, str]:
        """Return history buffer."""

        buffer: Any = self.buffer[-self.k * 2 :] if self.k > 0 else []
        if not self.return_messages:
            buffer = get_buffer_string(
                buffer,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
        return {self.memory_key: buffer}