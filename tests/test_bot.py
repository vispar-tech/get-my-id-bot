"""
Tests for the Telegram bot.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes

from bot import start_command, help_command, handle_message


@pytest.fixture
def mock_update() -> Mock:
    """Create a mock update object."""
    update = Mock(spec=Update)
    update.effective_user = Mock(spec=User)
    update.effective_user.id = 123456789
    update.effective_user.username = "testuser"

    update.effective_chat = Mock(spec=Chat)
    update.effective_chat.id = 987654321

    update.message = Mock(spec=Message)
    update.message.reply_text = AsyncMock()

    return update


@pytest.fixture
def mock_context() -> Mock:
    """Create a mock context object."""
    return Mock(spec=ContextTypes.DEFAULT_TYPE)


@pytest.mark.asyncio
async def test_start_command(mock_update: Mock, mock_context: Mock) -> None:
    """Test /start command."""
    await start_command(mock_update, mock_context)

    # Verify reply_text was called
    mock_update.message.reply_text.assert_called_once()

    # Check the response contains user ID and chat ID
    call_args: str = mock_update.message.reply_text.call_args[0][0]
    assert "123456789" in call_args  # User ID
    assert "987654321" in call_args  # Chat ID


@pytest.mark.asyncio
async def test_help_command(mock_update: Mock, mock_context: Mock) -> None:
    """Test /help command."""
    await help_command(mock_update, mock_context)

    # Verify reply_text was called
    mock_update.message.reply_text.assert_called_once()

    # Check the response contains help information
    call_args: str = mock_update.message.reply_text.call_args[0][0]
    assert "telegram user ID" in call_args
    assert "/start" in call_args
    assert "/help" in call_args


@pytest.mark.asyncio
async def test_handle_message_basic(mock_update: Mock, mock_context: Mock) -> None:
    """Test handling of basic message."""
    await handle_message(mock_update, mock_context)

    # Verify reply_text was called
    mock_update.message.reply_text.assert_called_once()

    # Check the response contains basic IDs
    call_args: str = mock_update.message.reply_text.call_args[0][0]
    assert "123456789" in call_args  # User ID
    assert "987654321" in call_args  # Chat ID


@pytest.mark.asyncio
async def test_handle_forwarded_message(mock_update: Mock, mock_context: Mock) -> None:
    """Test handling of forwarded message."""
    # Add forwarded user
    forwarded_user = Mock(spec=User)
    forwarded_user.id = 111222333
    forwarded_user.username = "forwardeduser"

    mock_update.message.forward_from = forwarded_user

    await handle_message(mock_update, mock_context)

    # Verify reply_text was called
    mock_update.message.reply_text.assert_called_once()

    # Check the response contains forwarded user info
    call_args: str = mock_update.message.reply_text.call_args[0][0]
    assert "111222333" in call_args  # Forwarded user ID
    assert "@forwardeduser" in call_args  # Forwarded username
