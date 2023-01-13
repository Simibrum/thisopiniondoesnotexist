"""Test TextGenerator class."""
from app.backend.gpt import TextGenerator, API_KEY


def test_text_generator_mock(mocker):
    # Mock the Completion object
    mock_completion = mocker.MagicMock()
    mock_completion.choices = [mocker.MagicMock(text="completion text")]

    # Mock the Completion.create method
    mock_create = mocker.MagicMock(return_value=mock_completion)
    mocker.patch("openai.Completion.create", mock_create)

    # Create a Completion instance
    completion = TextGenerator()

    # Call the complete method
    result = completion.complete("prompt")

    # Assert that the create method was called with the correct arguments
    mock_create.assert_called_with(model="text-davinci-003", prompt="prompt", max_tokens=1024, temperature=0.5)

    # Assert that the correct completion text was returned
    assert result == "completion text"


def test_text_generator_live():
    """Test TextGenerator class with live API call."""
    completion = TextGenerator()
    result = completion.complete("Output some test text", max_tokens=10)
    print(result)
    assert result
    assert isinstance(result, str)