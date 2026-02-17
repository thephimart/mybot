"""Chat channels module with plugin architecture."""

from mybot.channels.base import BaseChannel
from mybot.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
